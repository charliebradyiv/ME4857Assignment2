// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from sr_interfaces:action/NavigateToWaypoint.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "sr_interfaces/action/navigate_to_waypoint.hpp"


#ifndef SR_INTERFACES__ACTION__DETAIL__NAVIGATE_TO_WAYPOINT__BUILDER_HPP_
#define SR_INTERFACES__ACTION__DETAIL__NAVIGATE_TO_WAYPOINT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "sr_interfaces/action/detail/navigate_to_waypoint__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace sr_interfaces
{

namespace action
{

namespace builder
{

class Init_NavigateToWaypoint_Goal_stop_distance
{
public:
  explicit Init_NavigateToWaypoint_Goal_stop_distance(::sr_interfaces::action::NavigateToWaypoint_Goal & msg)
  : msg_(msg)
  {}
  ::sr_interfaces::action::NavigateToWaypoint_Goal stop_distance(::sr_interfaces::action::NavigateToWaypoint_Goal::_stop_distance_type arg)
  {
    msg_.stop_distance = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_Goal msg_;
};

class Init_NavigateToWaypoint_Goal_target_name
{
public:
  Init_NavigateToWaypoint_Goal_target_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_NavigateToWaypoint_Goal_stop_distance target_name(::sr_interfaces::action::NavigateToWaypoint_Goal::_target_name_type arg)
  {
    msg_.target_name = std::move(arg);
    return Init_NavigateToWaypoint_Goal_stop_distance(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::sr_interfaces::action::NavigateToWaypoint_Goal>()
{
  return sr_interfaces::action::builder::Init_NavigateToWaypoint_Goal_target_name();
}

}  // namespace sr_interfaces


namespace sr_interfaces
{

namespace action
{

namespace builder
{

class Init_NavigateToWaypoint_Result_message
{
public:
  explicit Init_NavigateToWaypoint_Result_message(::sr_interfaces::action::NavigateToWaypoint_Result & msg)
  : msg_(msg)
  {}
  ::sr_interfaces::action::NavigateToWaypoint_Result message(::sr_interfaces::action::NavigateToWaypoint_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_Result msg_;
};

class Init_NavigateToWaypoint_Result_success
{
public:
  Init_NavigateToWaypoint_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_NavigateToWaypoint_Result_message success(::sr_interfaces::action::NavigateToWaypoint_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_NavigateToWaypoint_Result_message(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::sr_interfaces::action::NavigateToWaypoint_Result>()
{
  return sr_interfaces::action::builder::Init_NavigateToWaypoint_Result_success();
}

}  // namespace sr_interfaces


namespace sr_interfaces
{

namespace action
{

namespace builder
{

class Init_NavigateToWaypoint_Feedback_distance_remaining
{
public:
  Init_NavigateToWaypoint_Feedback_distance_remaining()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::sr_interfaces::action::NavigateToWaypoint_Feedback distance_remaining(::sr_interfaces::action::NavigateToWaypoint_Feedback::_distance_remaining_type arg)
  {
    msg_.distance_remaining = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::sr_interfaces::action::NavigateToWaypoint_Feedback>()
{
  return sr_interfaces::action::builder::Init_NavigateToWaypoint_Feedback_distance_remaining();
}

}  // namespace sr_interfaces


namespace sr_interfaces
{

namespace action
{

namespace builder
{

class Init_NavigateToWaypoint_SendGoal_Request_goal
{
public:
  explicit Init_NavigateToWaypoint_SendGoal_Request_goal(::sr_interfaces::action::NavigateToWaypoint_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::sr_interfaces::action::NavigateToWaypoint_SendGoal_Request goal(::sr_interfaces::action::NavigateToWaypoint_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_SendGoal_Request msg_;
};

class Init_NavigateToWaypoint_SendGoal_Request_goal_id
{
public:
  Init_NavigateToWaypoint_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_NavigateToWaypoint_SendGoal_Request_goal goal_id(::sr_interfaces::action::NavigateToWaypoint_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_NavigateToWaypoint_SendGoal_Request_goal(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::sr_interfaces::action::NavigateToWaypoint_SendGoal_Request>()
{
  return sr_interfaces::action::builder::Init_NavigateToWaypoint_SendGoal_Request_goal_id();
}

}  // namespace sr_interfaces


namespace sr_interfaces
{

namespace action
{

namespace builder
{

class Init_NavigateToWaypoint_SendGoal_Response_stamp
{
public:
  explicit Init_NavigateToWaypoint_SendGoal_Response_stamp(::sr_interfaces::action::NavigateToWaypoint_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::sr_interfaces::action::NavigateToWaypoint_SendGoal_Response stamp(::sr_interfaces::action::NavigateToWaypoint_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_SendGoal_Response msg_;
};

class Init_NavigateToWaypoint_SendGoal_Response_accepted
{
public:
  Init_NavigateToWaypoint_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_NavigateToWaypoint_SendGoal_Response_stamp accepted(::sr_interfaces::action::NavigateToWaypoint_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_NavigateToWaypoint_SendGoal_Response_stamp(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::sr_interfaces::action::NavigateToWaypoint_SendGoal_Response>()
{
  return sr_interfaces::action::builder::Init_NavigateToWaypoint_SendGoal_Response_accepted();
}

}  // namespace sr_interfaces


namespace sr_interfaces
{

namespace action
{

namespace builder
{

class Init_NavigateToWaypoint_SendGoal_Event_response
{
public:
  explicit Init_NavigateToWaypoint_SendGoal_Event_response(::sr_interfaces::action::NavigateToWaypoint_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::sr_interfaces::action::NavigateToWaypoint_SendGoal_Event response(::sr_interfaces::action::NavigateToWaypoint_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_SendGoal_Event msg_;
};

class Init_NavigateToWaypoint_SendGoal_Event_request
{
public:
  explicit Init_NavigateToWaypoint_SendGoal_Event_request(::sr_interfaces::action::NavigateToWaypoint_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_NavigateToWaypoint_SendGoal_Event_response request(::sr_interfaces::action::NavigateToWaypoint_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_NavigateToWaypoint_SendGoal_Event_response(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_SendGoal_Event msg_;
};

class Init_NavigateToWaypoint_SendGoal_Event_info
{
public:
  Init_NavigateToWaypoint_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_NavigateToWaypoint_SendGoal_Event_request info(::sr_interfaces::action::NavigateToWaypoint_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_NavigateToWaypoint_SendGoal_Event_request(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::sr_interfaces::action::NavigateToWaypoint_SendGoal_Event>()
{
  return sr_interfaces::action::builder::Init_NavigateToWaypoint_SendGoal_Event_info();
}

}  // namespace sr_interfaces


namespace sr_interfaces
{

namespace action
{

namespace builder
{

class Init_NavigateToWaypoint_GetResult_Request_goal_id
{
public:
  Init_NavigateToWaypoint_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::sr_interfaces::action::NavigateToWaypoint_GetResult_Request goal_id(::sr_interfaces::action::NavigateToWaypoint_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::sr_interfaces::action::NavigateToWaypoint_GetResult_Request>()
{
  return sr_interfaces::action::builder::Init_NavigateToWaypoint_GetResult_Request_goal_id();
}

}  // namespace sr_interfaces


namespace sr_interfaces
{

namespace action
{

namespace builder
{

class Init_NavigateToWaypoint_GetResult_Response_result
{
public:
  explicit Init_NavigateToWaypoint_GetResult_Response_result(::sr_interfaces::action::NavigateToWaypoint_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::sr_interfaces::action::NavigateToWaypoint_GetResult_Response result(::sr_interfaces::action::NavigateToWaypoint_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_GetResult_Response msg_;
};

class Init_NavigateToWaypoint_GetResult_Response_status
{
public:
  Init_NavigateToWaypoint_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_NavigateToWaypoint_GetResult_Response_result status(::sr_interfaces::action::NavigateToWaypoint_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_NavigateToWaypoint_GetResult_Response_result(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::sr_interfaces::action::NavigateToWaypoint_GetResult_Response>()
{
  return sr_interfaces::action::builder::Init_NavigateToWaypoint_GetResult_Response_status();
}

}  // namespace sr_interfaces


namespace sr_interfaces
{

namespace action
{

namespace builder
{

class Init_NavigateToWaypoint_GetResult_Event_response
{
public:
  explicit Init_NavigateToWaypoint_GetResult_Event_response(::sr_interfaces::action::NavigateToWaypoint_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::sr_interfaces::action::NavigateToWaypoint_GetResult_Event response(::sr_interfaces::action::NavigateToWaypoint_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_GetResult_Event msg_;
};

class Init_NavigateToWaypoint_GetResult_Event_request
{
public:
  explicit Init_NavigateToWaypoint_GetResult_Event_request(::sr_interfaces::action::NavigateToWaypoint_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_NavigateToWaypoint_GetResult_Event_response request(::sr_interfaces::action::NavigateToWaypoint_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_NavigateToWaypoint_GetResult_Event_response(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_GetResult_Event msg_;
};

class Init_NavigateToWaypoint_GetResult_Event_info
{
public:
  Init_NavigateToWaypoint_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_NavigateToWaypoint_GetResult_Event_request info(::sr_interfaces::action::NavigateToWaypoint_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_NavigateToWaypoint_GetResult_Event_request(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::sr_interfaces::action::NavigateToWaypoint_GetResult_Event>()
{
  return sr_interfaces::action::builder::Init_NavigateToWaypoint_GetResult_Event_info();
}

}  // namespace sr_interfaces


namespace sr_interfaces
{

namespace action
{

namespace builder
{

class Init_NavigateToWaypoint_FeedbackMessage_feedback
{
public:
  explicit Init_NavigateToWaypoint_FeedbackMessage_feedback(::sr_interfaces::action::NavigateToWaypoint_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::sr_interfaces::action::NavigateToWaypoint_FeedbackMessage feedback(::sr_interfaces::action::NavigateToWaypoint_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_FeedbackMessage msg_;
};

class Init_NavigateToWaypoint_FeedbackMessage_goal_id
{
public:
  Init_NavigateToWaypoint_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_NavigateToWaypoint_FeedbackMessage_feedback goal_id(::sr_interfaces::action::NavigateToWaypoint_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_NavigateToWaypoint_FeedbackMessage_feedback(msg_);
  }

private:
  ::sr_interfaces::action::NavigateToWaypoint_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::sr_interfaces::action::NavigateToWaypoint_FeedbackMessage>()
{
  return sr_interfaces::action::builder::Init_NavigateToWaypoint_FeedbackMessage_goal_id();
}

}  // namespace sr_interfaces

#endif  // SR_INTERFACES__ACTION__DETAIL__NAVIGATE_TO_WAYPOINT__BUILDER_HPP_
