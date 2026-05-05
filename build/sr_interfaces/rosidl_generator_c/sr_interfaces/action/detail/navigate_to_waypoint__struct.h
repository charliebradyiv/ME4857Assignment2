// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from sr_interfaces:action/NavigateToWaypoint.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "sr_interfaces/action/navigate_to_waypoint.h"


#ifndef SR_INTERFACES__ACTION__DETAIL__NAVIGATE_TO_WAYPOINT__STRUCT_H_
#define SR_INTERFACES__ACTION__DETAIL__NAVIGATE_TO_WAYPOINT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'target_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/NavigateToWaypoint in the package sr_interfaces.
typedef struct sr_interfaces__action__NavigateToWaypoint_Goal
{
  rosidl_runtime_c__String target_name;
  double stop_distance;
} sr_interfaces__action__NavigateToWaypoint_Goal;

// Struct for a sequence of sr_interfaces__action__NavigateToWaypoint_Goal.
typedef struct sr_interfaces__action__NavigateToWaypoint_Goal__Sequence
{
  sr_interfaces__action__NavigateToWaypoint_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sr_interfaces__action__NavigateToWaypoint_Goal__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/NavigateToWaypoint in the package sr_interfaces.
typedef struct sr_interfaces__action__NavigateToWaypoint_Result
{
  bool success;
  rosidl_runtime_c__String message;
} sr_interfaces__action__NavigateToWaypoint_Result;

// Struct for a sequence of sr_interfaces__action__NavigateToWaypoint_Result.
typedef struct sr_interfaces__action__NavigateToWaypoint_Result__Sequence
{
  sr_interfaces__action__NavigateToWaypoint_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sr_interfaces__action__NavigateToWaypoint_Result__Sequence;

// Constants defined in the message

/// Struct defined in action/NavigateToWaypoint in the package sr_interfaces.
typedef struct sr_interfaces__action__NavigateToWaypoint_Feedback
{
  double distance_remaining;
} sr_interfaces__action__NavigateToWaypoint_Feedback;

// Struct for a sequence of sr_interfaces__action__NavigateToWaypoint_Feedback.
typedef struct sr_interfaces__action__NavigateToWaypoint_Feedback__Sequence
{
  sr_interfaces__action__NavigateToWaypoint_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sr_interfaces__action__NavigateToWaypoint_Feedback__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "sr_interfaces/action/detail/navigate_to_waypoint__struct.h"

/// Struct defined in action/NavigateToWaypoint in the package sr_interfaces.
typedef struct sr_interfaces__action__NavigateToWaypoint_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  sr_interfaces__action__NavigateToWaypoint_Goal goal;
} sr_interfaces__action__NavigateToWaypoint_SendGoal_Request;

// Struct for a sequence of sr_interfaces__action__NavigateToWaypoint_SendGoal_Request.
typedef struct sr_interfaces__action__NavigateToWaypoint_SendGoal_Request__Sequence
{
  sr_interfaces__action__NavigateToWaypoint_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sr_interfaces__action__NavigateToWaypoint_SendGoal_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/NavigateToWaypoint in the package sr_interfaces.
typedef struct sr_interfaces__action__NavigateToWaypoint_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} sr_interfaces__action__NavigateToWaypoint_SendGoal_Response;

// Struct for a sequence of sr_interfaces__action__NavigateToWaypoint_SendGoal_Response.
typedef struct sr_interfaces__action__NavigateToWaypoint_SendGoal_Response__Sequence
{
  sr_interfaces__action__NavigateToWaypoint_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sr_interfaces__action__NavigateToWaypoint_SendGoal_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  sr_interfaces__action__NavigateToWaypoint_SendGoal_Event__request__MAX_SIZE = 1
};
// response
enum
{
  sr_interfaces__action__NavigateToWaypoint_SendGoal_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/NavigateToWaypoint in the package sr_interfaces.
typedef struct sr_interfaces__action__NavigateToWaypoint_SendGoal_Event
{
  service_msgs__msg__ServiceEventInfo info;
  sr_interfaces__action__NavigateToWaypoint_SendGoal_Request__Sequence request;
  sr_interfaces__action__NavigateToWaypoint_SendGoal_Response__Sequence response;
} sr_interfaces__action__NavigateToWaypoint_SendGoal_Event;

// Struct for a sequence of sr_interfaces__action__NavigateToWaypoint_SendGoal_Event.
typedef struct sr_interfaces__action__NavigateToWaypoint_SendGoal_Event__Sequence
{
  sr_interfaces__action__NavigateToWaypoint_SendGoal_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sr_interfaces__action__NavigateToWaypoint_SendGoal_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/NavigateToWaypoint in the package sr_interfaces.
typedef struct sr_interfaces__action__NavigateToWaypoint_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} sr_interfaces__action__NavigateToWaypoint_GetResult_Request;

// Struct for a sequence of sr_interfaces__action__NavigateToWaypoint_GetResult_Request.
typedef struct sr_interfaces__action__NavigateToWaypoint_GetResult_Request__Sequence
{
  sr_interfaces__action__NavigateToWaypoint_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sr_interfaces__action__NavigateToWaypoint_GetResult_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__struct.h"

/// Struct defined in action/NavigateToWaypoint in the package sr_interfaces.
typedef struct sr_interfaces__action__NavigateToWaypoint_GetResult_Response
{
  int8_t status;
  sr_interfaces__action__NavigateToWaypoint_Result result;
} sr_interfaces__action__NavigateToWaypoint_GetResult_Response;

// Struct for a sequence of sr_interfaces__action__NavigateToWaypoint_GetResult_Response.
typedef struct sr_interfaces__action__NavigateToWaypoint_GetResult_Response__Sequence
{
  sr_interfaces__action__NavigateToWaypoint_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sr_interfaces__action__NavigateToWaypoint_GetResult_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  sr_interfaces__action__NavigateToWaypoint_GetResult_Event__request__MAX_SIZE = 1
};
// response
enum
{
  sr_interfaces__action__NavigateToWaypoint_GetResult_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/NavigateToWaypoint in the package sr_interfaces.
typedef struct sr_interfaces__action__NavigateToWaypoint_GetResult_Event
{
  service_msgs__msg__ServiceEventInfo info;
  sr_interfaces__action__NavigateToWaypoint_GetResult_Request__Sequence request;
  sr_interfaces__action__NavigateToWaypoint_GetResult_Response__Sequence response;
} sr_interfaces__action__NavigateToWaypoint_GetResult_Event;

// Struct for a sequence of sr_interfaces__action__NavigateToWaypoint_GetResult_Event.
typedef struct sr_interfaces__action__NavigateToWaypoint_GetResult_Event__Sequence
{
  sr_interfaces__action__NavigateToWaypoint_GetResult_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sr_interfaces__action__NavigateToWaypoint_GetResult_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__struct.h"

/// Struct defined in action/NavigateToWaypoint in the package sr_interfaces.
typedef struct sr_interfaces__action__NavigateToWaypoint_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  sr_interfaces__action__NavigateToWaypoint_Feedback feedback;
} sr_interfaces__action__NavigateToWaypoint_FeedbackMessage;

// Struct for a sequence of sr_interfaces__action__NavigateToWaypoint_FeedbackMessage.
typedef struct sr_interfaces__action__NavigateToWaypoint_FeedbackMessage__Sequence
{
  sr_interfaces__action__NavigateToWaypoint_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sr_interfaces__action__NavigateToWaypoint_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SR_INTERFACES__ACTION__DETAIL__NAVIGATE_TO_WAYPOINT__STRUCT_H_
