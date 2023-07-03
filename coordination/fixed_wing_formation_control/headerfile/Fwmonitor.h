// Generated by gencpp from file fixed_wing_formation_control/Fwmonitor.msg
// DO NOT EDIT!


#ifndef FIXED_WING_FORMATION_CONTROL_MESSAGE_FWMONITOR_H
#define FIXED_WING_FORMATION_CONTROL_MESSAGE_FWMONITOR_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace fixed_wing_formation_control
{
template <class ContainerAllocator>
struct Fwmonitor_
{
  typedef Fwmonitor_<ContainerAllocator> Type;

  Fwmonitor_()
    : planeID(0)
    , fw_complete_idel(false)
    , fw_is_connected(false)
    , fw_is_wellctrlled(false)
    , fw_complete_takeoff(false)
    , fw_complete_landed(false)
    , formation_distance_complete(false)
    , formation_time_complete(false)  {
    }
  Fwmonitor_(const ContainerAllocator& _alloc)
    : planeID(0)
    , fw_complete_idel(false)
    , fw_is_connected(false)
    , fw_is_wellctrlled(false)
    , fw_complete_takeoff(false)
    , fw_complete_landed(false)
    , formation_distance_complete(false)
    , formation_time_complete(false)  {
  (void)_alloc;
    }



   typedef uint8_t _planeID_type;
  _planeID_type planeID;

   typedef uint8_t _fw_complete_idel_type;
  _fw_complete_idel_type fw_complete_idel;

   typedef uint8_t _fw_is_connected_type;
  _fw_is_connected_type fw_is_connected;

   typedef uint8_t _fw_is_wellctrlled_type;
  _fw_is_wellctrlled_type fw_is_wellctrlled;

   typedef uint8_t _fw_complete_takeoff_type;
  _fw_complete_takeoff_type fw_complete_takeoff;

   typedef uint8_t _fw_complete_landed_type;
  _fw_complete_landed_type fw_complete_landed;

   typedef uint8_t _formation_distance_complete_type;
  _formation_distance_complete_type formation_distance_complete;

   typedef uint8_t _formation_time_complete_type;
  _formation_time_complete_type formation_time_complete;





  typedef boost::shared_ptr< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> const> ConstPtr;

}; // struct Fwmonitor_

typedef ::fixed_wing_formation_control::Fwmonitor_<std::allocator<void> > Fwmonitor;

typedef boost::shared_ptr< ::fixed_wing_formation_control::Fwmonitor > FwmonitorPtr;
typedef boost::shared_ptr< ::fixed_wing_formation_control::Fwmonitor const> FwmonitorConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator1> & lhs, const ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator2> & rhs)
{
  return lhs.planeID == rhs.planeID &&
    lhs.fw_complete_idel == rhs.fw_complete_idel &&
    lhs.fw_is_connected == rhs.fw_is_connected &&
    lhs.fw_is_wellctrlled == rhs.fw_is_wellctrlled &&
    lhs.fw_complete_takeoff == rhs.fw_complete_takeoff &&
    lhs.fw_complete_landed == rhs.fw_complete_landed &&
    lhs.formation_distance_complete == rhs.formation_distance_complete &&
    lhs.formation_time_complete == rhs.formation_time_complete;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator1> & lhs, const ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace fixed_wing_formation_control

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> >
{
  static const char* value()
  {
    return "3094edf1d529e87912463a6fbc28d66c";
  }

  static const char* value(const ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x3094edf1d529e879ULL;
  static const uint64_t static_value2 = 0x12463a6fbc28d66cULL;
};

template<class ContainerAllocator>
struct DataType< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> >
{
  static const char* value()
  {
    return "fixed_wing_formation_control/Fwmonitor";
  }

  static const char* value(const ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> >
{
  static const char* value()
  {
    return "#飞机的控制状态，任务状态的flags，表示任务完成状况，飞机的飞行状态，失联状态，\n"
"#飞机控制保护状态\n"
"\n"
"uint8 planeID#飞机编号\n"
"\n"
"bool fw_complete_idel#飞机已经空闲\n"
"\n"
"bool fw_is_connected #飞机链接地面站标志位\n"
"\n"
"bool fw_is_wellctrlled #飞机控制状态标志位\n"
"\n"
"bool fw_complete_takeoff #飞机已经起飞标志位\n"
"\n"
"bool fw_complete_landed #飞机已经降落标志位\n"
"\n"
"bool formation_distance_complete #飞机编队距离已经满足\n"
"\n"
"bool formation_time_complete #飞机编队时间已经满足\n"
;
  }

  static const char* value(const ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.planeID);
      stream.next(m.fw_complete_idel);
      stream.next(m.fw_is_connected);
      stream.next(m.fw_is_wellctrlled);
      stream.next(m.fw_complete_takeoff);
      stream.next(m.fw_complete_landed);
      stream.next(m.formation_distance_complete);
      stream.next(m.formation_time_complete);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Fwmonitor_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::fixed_wing_formation_control::Fwmonitor_<ContainerAllocator>& v)
  {
    s << indent << "planeID: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.planeID);
    s << indent << "fw_complete_idel: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.fw_complete_idel);
    s << indent << "fw_is_connected: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.fw_is_connected);
    s << indent << "fw_is_wellctrlled: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.fw_is_wellctrlled);
    s << indent << "fw_complete_takeoff: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.fw_complete_takeoff);
    s << indent << "fw_complete_landed: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.fw_complete_landed);
    s << indent << "formation_distance_complete: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.formation_distance_complete);
    s << indent << "formation_time_complete: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.formation_time_complete);
  }
};

} // namespace message_operations
} // namespace ros

#endif // FIXED_WING_FORMATION_CONTROL_MESSAGE_FWMONITOR_H
