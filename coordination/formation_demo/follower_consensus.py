#!/usr/bin/python
# -*- coding: UTF-8 -*-
### This code is about the distributed formation control of consensus protocol with a certain
### Laplacian matrix and the formation transformation based on a task allocation algorithm——
### KM for the shorest distances of all the UAVs to achieve the new pattern.
### For more information of these two algorithms, please see the paper on https://arxiv.org/abs/2005.01125

import rospy
from geometry_msgs.msg import Twist, Vector3, PoseStamped, TwistStamped
from std_msgs.msg import String
import sys
import numpy

# formation patterns
if sys.argv[3] == '6':
    from formation_dict import formation_dict_6 as formation_dict
elif sys.argv[3] == '9':
    from formation_dict import formation_dict_9 as formation_dict
elif sys.argv[3] == '18':
    from formation_dict import formation_dict_18 as formation_dict

class Follower:
    def __init__(self, uav_type, uav_id, uav_num):
        self.uav_type = uav_type
        self.id = uav_id
        self.uav_num = uav_num
        self.f = 30  # control/communication rate
        self.cmd_vel_enu = Twist()
        self.avoid_vel = Vector3()
        self.following_ids = []  # followers of this uav
        self.formation_config = 'waiting'
        self.following_count = 1  # the number of followers of this uav
        self.L_matrix = None
        self.Kp = 1.0
        self.vel_max = 1
        self.local_pose = [PoseStamped() for i in range(self.uav_num)]
        self.local_velocity = [TwistStamped() for i in range(self.uav_num)]
        self.local_pose_sub = [[] for i in range(self.uav_num)]
        self.local_velocity_sub = [[] for i in range(self.uav_num)]
        self.omega = 1.0
        self.gamma = 1.0
        self.avoid_vel_sub = rospy.Subscriber("/xtdrone/" + self.uav_type + '_' + str(self.id) + "/avoid_vel", Vector3, self.avoid_vel_callback,queue_size=1)
        self.formation_switch_sub = rospy.Subscriber("/xtdrone/formation_switch", String, self.formation_switch_callback, queue_size=1)
        self.vel_enu_pub = rospy.Publisher('/xtdrone/' + self.uav_type + '_' + str(self.id) + '/cmd_vel_enu', Twist, queue_size=1)
        self.info_pub = rospy.Publisher('/xtdrone/' + self.uav_type + '_' + str(self.id) + '/info', String, queue_size=1)
        self.cmd_pub = rospy.Publisher('/xtdrone/' + self.uav_type + '_' + str(self.id) + '/cmd', String, queue_size=1)
        for i in range(self.uav_num):
            self.local_pose_sub[i] = rospy.Subscriber(
                self.uav_type + '_' + str(i) + "/mavros/local_position/pose", PoseStamped,
                self.local_pose_callback, i, queue_size=1)
        for i in range(self.uav_num):
            self.local_velocity_sub[i] = rospy.Subscriber(
                self.uav_type + '_' + str(i) + "/mavros/local_position/velocity_local", TwistStamped,
                self.local_twist_callback, i, queue_size=1)
        self.wait_cmd = 'HOVER'
        self.orig_formation = formation_dict["origin"]
        self.new_formation = None

    def local_pose_callback(self, msg, id):
        self.local_pose[id] = msg
    
    def local_twist_callback(self, msg, id):
        self.local_velocity[id] = msg

        # the order of changing the formation pattern

    def formation_switch_callback(self, msg):
        if not self.formation_config == msg.data:
            self.formation_config = msg.data
            print("Follower"+str(self.id-1)+": Switch to Formation " + msg.data)
            if self.formation_config == 'waiting':
                self.cmd_pub.publish(self.wait_cmd)
            else:
                self.adj_matrix = self.build_graph(self.orig_formation,
                                                    formation_dict[self.formation_config])
                # These variables are determined for KM algorithm
                self.label_left = numpy.max(self.adj_matrix, axis=1)  # init label for the left set
                self.label_right = numpy.array([0] * (self.uav_num - 1))  # init label for the right set
                self.match_right = numpy.array([-1] * (self.uav_num - 1))
                self.visit_left = numpy.array([0] * (self.uav_num - 1))
                self.visit_right = numpy.array([0] * (self.uav_num - 1))
                self.slack_right = numpy.array([100] * (self.uav_num - 1))
                self.change_id = self.KM()
                # Get a new formation pattern of UAVs based on KM.
                self.new_formation = self.get_new_formation(self.change_id,
                                                            formation_dict[self.formation_config])
                self.L_matrix = self.get_L_matrix(self.new_formation)
                self.orig_formation = self.new_formation

    def avoid_vel_callback(self, msg):
        self.avoid_vel = msg

    def loop(self):
        rospy.init_node('follower' + str(self.id - 1))
        rate = rospy.Rate(self.f)
        while not rospy.is_shutdown():
            if not self.formation_config == 'waiting' and not self.L_matrix is None:
                input = Vector3(0, 0, 0)
                # Get the local leaders of this UAV based on the Laplacian matrix
                self.following_ids = numpy.argwhere(self.L_matrix[self.id, :] == 1)
                self.following_ids = self.following_ids.reshape(self.following_ids.shape[0])
                self.following_count = len(self.following_ids)
                self.gamma = (4.0/self.following_count)**0.5
                for following_id in self.following_ids:
                    if following_id == 0: # following leader
                        input.x += self.local_pose[
                                        following_id].pose.position.x - self.local_pose[self.id].pose.position.x + \
                                    self.new_formation[0, self.id - 1] + self.gamma * (self.local_velocity[following_id].twist.linear.x - self.local_velocity[self.id].twist.linear.x)
                        input.y += self.local_pose[
                                        following_id].pose.position.y - self.local_pose[self.id].pose.position.y + \
                                    self.new_formation[1, self.id - 1] + self.gamma * (self.local_velocity[following_id].twist.linear.y - self.local_velocity[self.id].twist.linear.y)
                        input.z += self.local_pose[
                                        following_id].pose.position.z - self.local_pose[self.id].pose.position.z + \
                                    self.new_formation[2, self.id - 1] + self.gamma * (self.local_velocity[following_id].twist.linear.z - self.local_velocity[self.id].twist.linear.z)
                    else:
                        input.x += self.local_pose[
                                                    following_id].pose.position.x - self.local_pose[self.id].pose.position.x + \
                                                self.new_formation[0, self.id - 1] - self.new_formation[0, following_id - 1] + self.gamma * (self.local_velocity[following_id].twist.linear.x - self.local_velocity[self.id].twist.linear.x)
                        input.y += self.local_pose[
                                                    following_id].pose.position.y - self.local_pose[self.id].pose.position.y + \
                                                self.new_formation[1, self.id - 1] - self.new_formation[1, following_id - 1] + self.gamma * (self.local_velocity[following_id].twist.linear.y - self.local_velocity[self.id].twist.linear.y)
                        input.z += self.local_pose[
                                                    following_id].pose.position.z - self.local_pose[self.id].pose.position.z + \
                                                self.new_formation[2, self.id - 1] - self.new_formation[2, following_id - 1] + self.gamma * (self.local_velocity[following_id].twist.linear.z - self.local_velocity[self.id].twist.linear.z)

                # self.omega = self.Kp/self.following_count
                # self.cmd_vel_enu.linear.x = self.omega * input_vel.x+ 1**0.5 * self.vel_max * self.avoid_vel.x
                # self.cmd_vel_enu.linear.y = self.omega * input_vel.y + 1**0.5 * self.vel_max * self.avoid_vel.y
                # self.cmd_vel_enu.linear.z = self.omega * input_vel.z + 1**0.5 * self.vel_max * self.avoid_vel.z 

                self.cmd_vel_enu.linear.x = self.local_velocity[self.id].twist.linear.x + 1.0/self.f * input.x + 1**0.5 * self.vel_max * self.avoid_vel.x
                self.cmd_vel_enu.linear.y = self.local_velocity[self.id].twist.linear.y + 1.0/self.f * input.y + 1**0.5 * self.vel_max * self.avoid_vel.y
                self.cmd_vel_enu.linear.z = self.local_velocity[self.id].twist.linear.z + 1.0/self.f * input.z + 1**0.5 * self.vel_max * self.avoid_vel.z 
                cmd_vel_magnitude = (self.cmd_vel_enu.linear.x**2 + self.cmd_vel_enu.linear.y**2 + self.cmd_vel_enu.linear.z**2)**0.5
                if cmd_vel_magnitude > 3**0.5 * self.vel_max:
                    self.cmd_vel_enu.linear.x = self.cmd_vel_enu.linear.x / cmd_vel_magnitude * self.vel_max
                    self.cmd_vel_enu.linear.y = self.cmd_vel_enu.linear.y / cmd_vel_magnitude * self.vel_max
                    self.cmd_vel_enu.linear.z = self.cmd_vel_enu.linear.z / cmd_vel_magnitude * self.vel_max

                self.vel_enu_pub.publish(self.cmd_vel_enu)

            rate.sleep()

    # 'build_graph',  'find_path' and 'KM' functions are all determined for KM algorithm.
    # A graph of UAVs is established based on distances between them in 'build_graph' function.
    def build_graph(self, orig_formation, change_formation):
        distance = [[0 for i in range(self.uav_num - 1)] for j in range(self.uav_num - 1)]
        for i in range(self.uav_num - 1):
            for j in range(self.uav_num - 1):
                distance[i][j] = numpy.linalg.norm(orig_formation[:, i] - change_formation[:, j])
                distance[i][j] = int(50 - distance[i][j])
        return distance

    # Determine whether a path has been found.
    def find_path(self, i):
        self.visit_left[i] = True
        for j, match_weight in enumerate(self.adj_matrix[i], start=0):
            if self.visit_right[j]:
                continue
            gap = self.label_left[i] + self.label_right[j] - match_weight
            if gap == 0:
                self.visit_right[j] = True
                if self.match_right[j] == -1 or self.find_path(self.match_right[j]):
                    self.match_right[j] = i
                    return True
            else:
                self.slack_right[j] = min(gap, self.slack_right[j])
        return False

    # Main body of KM algorithm.

    def KM(self):
        for i in range(self.uav_num - 1):
            self.slack_right = numpy.array([100] * (self.uav_num - 1))
            while True:
                self.visit_left = numpy.array([0] * (self.uav_num - 1))
                self.visit_right = numpy.array([0] * (self.uav_num - 1))
                if self.find_path(i):
                    break
                d = numpy.inf
                for j, slack in enumerate(self.slack_right):
                    if not self.visit_right[j]:
                        d = min(d, slack)
                for k in range(self.uav_num - 1):
                    if self.visit_left[k]:
                        self.label_left[k] -= d
                    if self.visit_right[k]:
                        self.label_right[k] += d
                    else:
                        self.slack_right[k] -= d
        return self.match_right

    # The formation patterns designed in the formation dictionaries are random (the old ones),
    # and a new formation pattern based on the distances of UAVs of the current pattern is designed as follows.
    # Note that only the desired position of each UAV has changed, while the form of the new pattern is the same as the one in the dictionary.
    def get_new_formation(self, change_id, change_formation):
        new_formation = numpy.zeros((3, self.uav_num - 1))
        position = numpy.zeros((3, self.uav_num - 1))
        change_id = [i + 1 for i in change_id]
        for i in range(0, self.uav_num - 1):
            position[:, i] = change_formation[:, i]

        for i in range(0, self.uav_num - 1):
            for j in range(0, self.uav_num - 1):
                if (j + 1) == change_id[i]:
                    new_formation[:, i] = position[:, j]
        return new_formation

    # Laplacian matrix

    def get_L_matrix(self, rel_posi):

        c_num = int((self.uav_num) / 2)
        min_num_index_list = [0] * c_num

        comm = [[] for i in range(self.uav_num)]
        w = numpy.ones((self.uav_num, self.uav_num)) * 0
        nodes_next = []
        node_flag = [self.uav_num - 1]
        node_mid_flag = []

        rel_d = [0] * (self.uav_num - 1)

        for i in range(0, self.uav_num - 1):
            rel_d[i] = pow(rel_posi[0][i], 2) + pow(rel_posi[1][i], 2) + pow(rel_posi[2][i], 2)

        c = numpy.copy(rel_d)
        c.sort()
        count = 0

        for j in range(0, c_num):
            for i in range(0, self.uav_num - 1):
                if rel_d[i] == c[j]:
                    if not i in node_mid_flag:
                        min_num_index_list[count] = i
                        node_mid_flag.append(i)
                        count = count + 1
                        if count == c_num:
                            break
            if count == c_num:
                break

        for j in range(0, c_num):
            nodes_next.append(min_num_index_list[j])

            comm[self.uav_num - 1].append(min_num_index_list[j])

        size_ = len(node_flag)

        while (nodes_next != []) and (size_ < (self.uav_num - 1)):

            next_node = nodes_next[0]
            nodes_next = nodes_next[1:]
            min_num_index_list = [0] * c_num
            node_mid_flag = []
            rel_d = [0] * (self.uav_num - 1)
            for i in range(0, self.uav_num - 1):

                if i == next_node or i in node_flag:

                    rel_d[i] = 2000
                else:

                    rel_d[i] = pow((rel_posi[0][i] - rel_posi[0][next_node]), 2) + pow(
                        (rel_posi[1][i] - rel_posi[1][next_node]), 2) + pow((rel_posi[2][i] - rel_posi[2][next_node]),
                                                                            2)
            c = numpy.copy(rel_d)
            c.sort()
            count = 0

            for j in range(0, c_num):
                for i in range(0, self.uav_num - 1):
                    if rel_d[i] == c[j]:
                        if not i in node_mid_flag:
                            min_num_index_list[count] = i
                            node_mid_flag.append(i)
                            count = count + 1
                            if count == c_num:
                                break
                if count == c_num:
                    break
            node_flag.append(next_node)

            size_ = len(node_flag)

            for j in range(0, c_num):

                if min_num_index_list[j] in node_flag:

                    nodes_next = nodes_next

                else:
                    if min_num_index_list[j] in nodes_next:
                        nodes_next = nodes_next
                    else:
                        nodes_next.append(min_num_index_list[j])

                    comm[next_node].append(min_num_index_list[j])

        for i in range(0, self.uav_num):
            for j in range(0, self.uav_num - 1):
                if i == 0:
                    if j in comm[self.uav_num - 1]:
                        w[j + 1][i] = 1
                    else:
                        w[j + 1][i] = 0
                else:
                    if j in comm[i - 1] and i < (j+1):
                        w[j + 1][i] = 1
                    else:
                        w[j + 1][i] = 0
            
        for i in range(1, self.uav_num):  # 防止某个无人机掉队
            if sum(w[i]) == 0:
                w[i][0] = 1
        L = w
        for i in range(0, self.uav_num):
            L[i][i] = -sum(w[i])
        return L

    def get_L_central_matrix(self):

        L = numpy.zeros((self.uav_num, self.uav_num))
        for i in range(1, self.uav_num):
            L[i][0] = 1
            L[i][i] = -1

        return L


if __name__ == '__main__':
    follower = Follower(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    follower.loop()
