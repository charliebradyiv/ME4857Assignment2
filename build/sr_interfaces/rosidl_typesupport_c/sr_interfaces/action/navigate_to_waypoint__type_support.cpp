// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from sr_interfaces:action/NavigateToWaypoint.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "sr_interfaces/action/detail/navigate_to_waypoint__struct.h"
#include "sr_interfaces/action/detail/navigate_to_waypoint__type_support.h"
#include "sr_interfaces/action/detail/navigate_to_waypoint__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace sr_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _NavigateToWaypoint_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NavigateToWaypoint_Goal_type_support_ids_t;

static const _NavigateToWaypoint_Goal_type_support_ids_t _NavigateToWaypoint_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _NavigateToWaypoint_Goal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NavigateToWaypoint_Goal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NavigateToWaypoint_Goal_type_support_symbol_names_t _NavigateToWaypoint_Goal_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sr_interfaces, action, NavigateToWaypoint_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sr_interfaces, action, NavigateToWaypoint_Goal)),
  }
};

typedef struct _NavigateToWaypoint_Goal_type_support_data_t
{
  void * data[2];
} _NavigateToWaypoint_Goal_type_support_data_t;

static _NavigateToWaypoint_Goal_type_support_data_t _NavigateToWaypoint_Goal_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NavigateToWaypoint_Goal_message_typesupport_map = {
  2,
  "sr_interfaces",
  &_NavigateToWaypoint_Goal_message_typesupport_ids.typesupport_identifier[0],
  &_NavigateToWaypoint_Goal_message_typesupport_symbol_names.symbol_name[0],
  &_NavigateToWaypoint_Goal_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t NavigateToWaypoint_Goal_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NavigateToWaypoint_Goal_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &sr_interfaces__action__NavigateToWaypoint_Goal__get_type_hash,
  &sr_interfaces__action__NavigateToWaypoint_Goal__get_type_description,
  &sr_interfaces__action__NavigateToWaypoint_Goal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace sr_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_Goal)() {
  return &::sr_interfaces::action::rosidl_typesupport_c::NavigateToWaypoint_Goal_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__type_support.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace sr_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _NavigateToWaypoint_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NavigateToWaypoint_Result_type_support_ids_t;

static const _NavigateToWaypoint_Result_type_support_ids_t _NavigateToWaypoint_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _NavigateToWaypoint_Result_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NavigateToWaypoint_Result_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NavigateToWaypoint_Result_type_support_symbol_names_t _NavigateToWaypoint_Result_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sr_interfaces, action, NavigateToWaypoint_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sr_interfaces, action, NavigateToWaypoint_Result)),
  }
};

typedef struct _NavigateToWaypoint_Result_type_support_data_t
{
  void * data[2];
} _NavigateToWaypoint_Result_type_support_data_t;

static _NavigateToWaypoint_Result_type_support_data_t _NavigateToWaypoint_Result_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NavigateToWaypoint_Result_message_typesupport_map = {
  2,
  "sr_interfaces",
  &_NavigateToWaypoint_Result_message_typesupport_ids.typesupport_identifier[0],
  &_NavigateToWaypoint_Result_message_typesupport_symbol_names.symbol_name[0],
  &_NavigateToWaypoint_Result_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t NavigateToWaypoint_Result_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NavigateToWaypoint_Result_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &sr_interfaces__action__NavigateToWaypoint_Result__get_type_hash,
  &sr_interfaces__action__NavigateToWaypoint_Result__get_type_description,
  &sr_interfaces__action__NavigateToWaypoint_Result__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace sr_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_Result)() {
  return &::sr_interfaces::action::rosidl_typesupport_c::NavigateToWaypoint_Result_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__type_support.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace sr_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _NavigateToWaypoint_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NavigateToWaypoint_Feedback_type_support_ids_t;

static const _NavigateToWaypoint_Feedback_type_support_ids_t _NavigateToWaypoint_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _NavigateToWaypoint_Feedback_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NavigateToWaypoint_Feedback_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NavigateToWaypoint_Feedback_type_support_symbol_names_t _NavigateToWaypoint_Feedback_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sr_interfaces, action, NavigateToWaypoint_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sr_interfaces, action, NavigateToWaypoint_Feedback)),
  }
};

typedef struct _NavigateToWaypoint_Feedback_type_support_data_t
{
  void * data[2];
} _NavigateToWaypoint_Feedback_type_support_data_t;

static _NavigateToWaypoint_Feedback_type_support_data_t _NavigateToWaypoint_Feedback_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NavigateToWaypoint_Feedback_message_typesupport_map = {
  2,
  "sr_interfaces",
  &_NavigateToWaypoint_Feedback_message_typesupport_ids.typesupport_identifier[0],
  &_NavigateToWaypoint_Feedback_message_typesupport_symbol_names.symbol_name[0],
  &_NavigateToWaypoint_Feedback_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t NavigateToWaypoint_Feedback_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NavigateToWaypoint_Feedback_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &sr_interfaces__action__NavigateToWaypoint_Feedback__get_type_hash,
  &sr_interfaces__action__NavigateToWaypoint_Feedback__get_type_description,
  &sr_interfaces__action__NavigateToWaypoint_Feedback__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace sr_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_Feedback)() {
  return &::sr_interfaces::action::rosidl_typesupport_c::NavigateToWaypoint_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__type_support.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace sr_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _NavigateToWaypoint_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NavigateToWaypoint_SendGoal_Request_type_support_ids_t;

static const _NavigateToWaypoint_SendGoal_Request_type_support_ids_t _NavigateToWaypoint_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _NavigateToWaypoint_SendGoal_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NavigateToWaypoint_SendGoal_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NavigateToWaypoint_SendGoal_Request_type_support_symbol_names_t _NavigateToWaypoint_SendGoal_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sr_interfaces, action, NavigateToWaypoint_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sr_interfaces, action, NavigateToWaypoint_SendGoal_Request)),
  }
};

typedef struct _NavigateToWaypoint_SendGoal_Request_type_support_data_t
{
  void * data[2];
} _NavigateToWaypoint_SendGoal_Request_type_support_data_t;

static _NavigateToWaypoint_SendGoal_Request_type_support_data_t _NavigateToWaypoint_SendGoal_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NavigateToWaypoint_SendGoal_Request_message_typesupport_map = {
  2,
  "sr_interfaces",
  &_NavigateToWaypoint_SendGoal_Request_message_typesupport_ids.typesupport_identifier[0],
  &_NavigateToWaypoint_SendGoal_Request_message_typesupport_symbol_names.symbol_name[0],
  &_NavigateToWaypoint_SendGoal_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t NavigateToWaypoint_SendGoal_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NavigateToWaypoint_SendGoal_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &sr_interfaces__action__NavigateToWaypoint_SendGoal_Request__get_type_hash,
  &sr_interfaces__action__NavigateToWaypoint_SendGoal_Request__get_type_description,
  &sr_interfaces__action__NavigateToWaypoint_SendGoal_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace sr_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_SendGoal_Request)() {
  return &::sr_interfaces::action::rosidl_typesupport_c::NavigateToWaypoint_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__type_support.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace sr_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _NavigateToWaypoint_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NavigateToWaypoint_SendGoal_Response_type_support_ids_t;

static const _NavigateToWaypoint_SendGoal_Response_type_support_ids_t _NavigateToWaypoint_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _NavigateToWaypoint_SendGoal_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NavigateToWaypoint_SendGoal_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NavigateToWaypoint_SendGoal_Response_type_support_symbol_names_t _NavigateToWaypoint_SendGoal_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sr_interfaces, action, NavigateToWaypoint_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sr_interfaces, action, NavigateToWaypoint_SendGoal_Response)),
  }
};

typedef struct _NavigateToWaypoint_SendGoal_Response_type_support_data_t
{
  void * data[2];
} _NavigateToWaypoint_SendGoal_Response_type_support_data_t;

static _NavigateToWaypoint_SendGoal_Response_type_support_data_t _NavigateToWaypoint_SendGoal_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NavigateToWaypoint_SendGoal_Response_message_typesupport_map = {
  2,
  "sr_interfaces",
  &_NavigateToWaypoint_SendGoal_Response_message_typesupport_ids.typesupport_identifier[0],
  &_NavigateToWaypoint_SendGoal_Response_message_typesupport_symbol_names.symbol_name[0],
  &_NavigateToWaypoint_SendGoal_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t NavigateToWaypoint_SendGoal_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NavigateToWaypoint_SendGoal_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &sr_interfaces__action__NavigateToWaypoint_SendGoal_Response__get_type_hash,
  &sr_interfaces__action__NavigateToWaypoint_SendGoal_Response__get_type_description,
  &sr_interfaces__action__NavigateToWaypoint_SendGoal_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace sr_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_SendGoal_Response)() {
  return &::sr_interfaces::action::rosidl_typesupport_c::NavigateToWaypoint_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__type_support.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace sr_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _NavigateToWaypoint_SendGoal_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NavigateToWaypoint_SendGoal_Event_type_support_ids_t;

static const _NavigateToWaypoint_SendGoal_Event_type_support_ids_t _NavigateToWaypoint_SendGoal_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _NavigateToWaypoint_SendGoal_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NavigateToWaypoint_SendGoal_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NavigateToWaypoint_SendGoal_Event_type_support_symbol_names_t _NavigateToWaypoint_SendGoal_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sr_interfaces, action, NavigateToWaypoint_SendGoal_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sr_interfaces, action, NavigateToWaypoint_SendGoal_Event)),
  }
};

typedef struct _NavigateToWaypoint_SendGoal_Event_type_support_data_t
{
  void * data[2];
} _NavigateToWaypoint_SendGoal_Event_type_support_data_t;

static _NavigateToWaypoint_SendGoal_Event_type_support_data_t _NavigateToWaypoint_SendGoal_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NavigateToWaypoint_SendGoal_Event_message_typesupport_map = {
  2,
  "sr_interfaces",
  &_NavigateToWaypoint_SendGoal_Event_message_typesupport_ids.typesupport_identifier[0],
  &_NavigateToWaypoint_SendGoal_Event_message_typesupport_symbol_names.symbol_name[0],
  &_NavigateToWaypoint_SendGoal_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t NavigateToWaypoint_SendGoal_Event_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NavigateToWaypoint_SendGoal_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &sr_interfaces__action__NavigateToWaypoint_SendGoal_Event__get_type_hash,
  &sr_interfaces__action__NavigateToWaypoint_SendGoal_Event__get_type_description,
  &sr_interfaces__action__NavigateToWaypoint_SendGoal_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace sr_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_SendGoal_Event)() {
  return &::sr_interfaces::action::rosidl_typesupport_c::NavigateToWaypoint_SendGoal_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
#include "service_msgs/msg/service_event_info.h"
#include "builtin_interfaces/msg/time.h"

namespace sr_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{
typedef struct _NavigateToWaypoint_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NavigateToWaypoint_SendGoal_type_support_ids_t;

static const _NavigateToWaypoint_SendGoal_type_support_ids_t _NavigateToWaypoint_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _NavigateToWaypoint_SendGoal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NavigateToWaypoint_SendGoal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NavigateToWaypoint_SendGoal_type_support_symbol_names_t _NavigateToWaypoint_SendGoal_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sr_interfaces, action, NavigateToWaypoint_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sr_interfaces, action, NavigateToWaypoint_SendGoal)),
  }
};

typedef struct _NavigateToWaypoint_SendGoal_type_support_data_t
{
  void * data[2];
} _NavigateToWaypoint_SendGoal_type_support_data_t;

static _NavigateToWaypoint_SendGoal_type_support_data_t _NavigateToWaypoint_SendGoal_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NavigateToWaypoint_SendGoal_service_typesupport_map = {
  2,
  "sr_interfaces",
  &_NavigateToWaypoint_SendGoal_service_typesupport_ids.typesupport_identifier[0],
  &_NavigateToWaypoint_SendGoal_service_typesupport_symbol_names.symbol_name[0],
  &_NavigateToWaypoint_SendGoal_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t NavigateToWaypoint_SendGoal_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NavigateToWaypoint_SendGoal_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &NavigateToWaypoint_SendGoal_Request_message_type_support_handle,
  &NavigateToWaypoint_SendGoal_Response_message_type_support_handle,
  &NavigateToWaypoint_SendGoal_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    sr_interfaces,
    action,
    NavigateToWaypoint_SendGoal
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    sr_interfaces,
    action,
    NavigateToWaypoint_SendGoal
  ),
  &sr_interfaces__action__NavigateToWaypoint_SendGoal__get_type_hash,
  &sr_interfaces__action__NavigateToWaypoint_SendGoal__get_type_description,
  &sr_interfaces__action__NavigateToWaypoint_SendGoal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace sr_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_SendGoal)() {
  return &::sr_interfaces::action::rosidl_typesupport_c::NavigateToWaypoint_SendGoal_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__type_support.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace sr_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _NavigateToWaypoint_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NavigateToWaypoint_GetResult_Request_type_support_ids_t;

static const _NavigateToWaypoint_GetResult_Request_type_support_ids_t _NavigateToWaypoint_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _NavigateToWaypoint_GetResult_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NavigateToWaypoint_GetResult_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NavigateToWaypoint_GetResult_Request_type_support_symbol_names_t _NavigateToWaypoint_GetResult_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sr_interfaces, action, NavigateToWaypoint_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sr_interfaces, action, NavigateToWaypoint_GetResult_Request)),
  }
};

typedef struct _NavigateToWaypoint_GetResult_Request_type_support_data_t
{
  void * data[2];
} _NavigateToWaypoint_GetResult_Request_type_support_data_t;

static _NavigateToWaypoint_GetResult_Request_type_support_data_t _NavigateToWaypoint_GetResult_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NavigateToWaypoint_GetResult_Request_message_typesupport_map = {
  2,
  "sr_interfaces",
  &_NavigateToWaypoint_GetResult_Request_message_typesupport_ids.typesupport_identifier[0],
  &_NavigateToWaypoint_GetResult_Request_message_typesupport_symbol_names.symbol_name[0],
  &_NavigateToWaypoint_GetResult_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t NavigateToWaypoint_GetResult_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NavigateToWaypoint_GetResult_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &sr_interfaces__action__NavigateToWaypoint_GetResult_Request__get_type_hash,
  &sr_interfaces__action__NavigateToWaypoint_GetResult_Request__get_type_description,
  &sr_interfaces__action__NavigateToWaypoint_GetResult_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace sr_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_GetResult_Request)() {
  return &::sr_interfaces::action::rosidl_typesupport_c::NavigateToWaypoint_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__type_support.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace sr_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _NavigateToWaypoint_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NavigateToWaypoint_GetResult_Response_type_support_ids_t;

static const _NavigateToWaypoint_GetResult_Response_type_support_ids_t _NavigateToWaypoint_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _NavigateToWaypoint_GetResult_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NavigateToWaypoint_GetResult_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NavigateToWaypoint_GetResult_Response_type_support_symbol_names_t _NavigateToWaypoint_GetResult_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sr_interfaces, action, NavigateToWaypoint_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sr_interfaces, action, NavigateToWaypoint_GetResult_Response)),
  }
};

typedef struct _NavigateToWaypoint_GetResult_Response_type_support_data_t
{
  void * data[2];
} _NavigateToWaypoint_GetResult_Response_type_support_data_t;

static _NavigateToWaypoint_GetResult_Response_type_support_data_t _NavigateToWaypoint_GetResult_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NavigateToWaypoint_GetResult_Response_message_typesupport_map = {
  2,
  "sr_interfaces",
  &_NavigateToWaypoint_GetResult_Response_message_typesupport_ids.typesupport_identifier[0],
  &_NavigateToWaypoint_GetResult_Response_message_typesupport_symbol_names.symbol_name[0],
  &_NavigateToWaypoint_GetResult_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t NavigateToWaypoint_GetResult_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NavigateToWaypoint_GetResult_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &sr_interfaces__action__NavigateToWaypoint_GetResult_Response__get_type_hash,
  &sr_interfaces__action__NavigateToWaypoint_GetResult_Response__get_type_description,
  &sr_interfaces__action__NavigateToWaypoint_GetResult_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace sr_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_GetResult_Response)() {
  return &::sr_interfaces::action::rosidl_typesupport_c::NavigateToWaypoint_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__type_support.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace sr_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _NavigateToWaypoint_GetResult_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NavigateToWaypoint_GetResult_Event_type_support_ids_t;

static const _NavigateToWaypoint_GetResult_Event_type_support_ids_t _NavigateToWaypoint_GetResult_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _NavigateToWaypoint_GetResult_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NavigateToWaypoint_GetResult_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NavigateToWaypoint_GetResult_Event_type_support_symbol_names_t _NavigateToWaypoint_GetResult_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sr_interfaces, action, NavigateToWaypoint_GetResult_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sr_interfaces, action, NavigateToWaypoint_GetResult_Event)),
  }
};

typedef struct _NavigateToWaypoint_GetResult_Event_type_support_data_t
{
  void * data[2];
} _NavigateToWaypoint_GetResult_Event_type_support_data_t;

static _NavigateToWaypoint_GetResult_Event_type_support_data_t _NavigateToWaypoint_GetResult_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NavigateToWaypoint_GetResult_Event_message_typesupport_map = {
  2,
  "sr_interfaces",
  &_NavigateToWaypoint_GetResult_Event_message_typesupport_ids.typesupport_identifier[0],
  &_NavigateToWaypoint_GetResult_Event_message_typesupport_symbol_names.symbol_name[0],
  &_NavigateToWaypoint_GetResult_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t NavigateToWaypoint_GetResult_Event_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NavigateToWaypoint_GetResult_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &sr_interfaces__action__NavigateToWaypoint_GetResult_Event__get_type_hash,
  &sr_interfaces__action__NavigateToWaypoint_GetResult_Event__get_type_description,
  &sr_interfaces__action__NavigateToWaypoint_GetResult_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace sr_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_GetResult_Event)() {
  return &::sr_interfaces::action::rosidl_typesupport_c::NavigateToWaypoint_GetResult_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "service_msgs/msg/service_event_info.h"
// already included above
// #include "builtin_interfaces/msg/time.h"

namespace sr_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{
typedef struct _NavigateToWaypoint_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NavigateToWaypoint_GetResult_type_support_ids_t;

static const _NavigateToWaypoint_GetResult_type_support_ids_t _NavigateToWaypoint_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _NavigateToWaypoint_GetResult_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NavigateToWaypoint_GetResult_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NavigateToWaypoint_GetResult_type_support_symbol_names_t _NavigateToWaypoint_GetResult_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sr_interfaces, action, NavigateToWaypoint_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sr_interfaces, action, NavigateToWaypoint_GetResult)),
  }
};

typedef struct _NavigateToWaypoint_GetResult_type_support_data_t
{
  void * data[2];
} _NavigateToWaypoint_GetResult_type_support_data_t;

static _NavigateToWaypoint_GetResult_type_support_data_t _NavigateToWaypoint_GetResult_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NavigateToWaypoint_GetResult_service_typesupport_map = {
  2,
  "sr_interfaces",
  &_NavigateToWaypoint_GetResult_service_typesupport_ids.typesupport_identifier[0],
  &_NavigateToWaypoint_GetResult_service_typesupport_symbol_names.symbol_name[0],
  &_NavigateToWaypoint_GetResult_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t NavigateToWaypoint_GetResult_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NavigateToWaypoint_GetResult_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &NavigateToWaypoint_GetResult_Request_message_type_support_handle,
  &NavigateToWaypoint_GetResult_Response_message_type_support_handle,
  &NavigateToWaypoint_GetResult_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    sr_interfaces,
    action,
    NavigateToWaypoint_GetResult
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    sr_interfaces,
    action,
    NavigateToWaypoint_GetResult
  ),
  &sr_interfaces__action__NavigateToWaypoint_GetResult__get_type_hash,
  &sr_interfaces__action__NavigateToWaypoint_GetResult__get_type_description,
  &sr_interfaces__action__NavigateToWaypoint_GetResult__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace sr_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_GetResult)() {
  return &::sr_interfaces::action::rosidl_typesupport_c::NavigateToWaypoint_GetResult_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__struct.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__type_support.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace sr_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _NavigateToWaypoint_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _NavigateToWaypoint_FeedbackMessage_type_support_ids_t;

static const _NavigateToWaypoint_FeedbackMessage_type_support_ids_t _NavigateToWaypoint_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _NavigateToWaypoint_FeedbackMessage_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _NavigateToWaypoint_FeedbackMessage_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _NavigateToWaypoint_FeedbackMessage_type_support_symbol_names_t _NavigateToWaypoint_FeedbackMessage_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sr_interfaces, action, NavigateToWaypoint_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sr_interfaces, action, NavigateToWaypoint_FeedbackMessage)),
  }
};

typedef struct _NavigateToWaypoint_FeedbackMessage_type_support_data_t
{
  void * data[2];
} _NavigateToWaypoint_FeedbackMessage_type_support_data_t;

static _NavigateToWaypoint_FeedbackMessage_type_support_data_t _NavigateToWaypoint_FeedbackMessage_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _NavigateToWaypoint_FeedbackMessage_message_typesupport_map = {
  2,
  "sr_interfaces",
  &_NavigateToWaypoint_FeedbackMessage_message_typesupport_ids.typesupport_identifier[0],
  &_NavigateToWaypoint_FeedbackMessage_message_typesupport_symbol_names.symbol_name[0],
  &_NavigateToWaypoint_FeedbackMessage_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t NavigateToWaypoint_FeedbackMessage_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_NavigateToWaypoint_FeedbackMessage_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &sr_interfaces__action__NavigateToWaypoint_FeedbackMessage__get_type_hash,
  &sr_interfaces__action__NavigateToWaypoint_FeedbackMessage__get_type_description,
  &sr_interfaces__action__NavigateToWaypoint_FeedbackMessage__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace sr_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_FeedbackMessage)() {
  return &::sr_interfaces::action::rosidl_typesupport_c::NavigateToWaypoint_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

#include "action_msgs/msg/goal_status_array.h"
#include "action_msgs/srv/cancel_goal.h"
#include "sr_interfaces/action/navigate_to_waypoint.h"
// already included above
// #include "sr_interfaces/action/detail/navigate_to_waypoint__type_support.h"

static rosidl_action_type_support_t _sr_interfaces__action__NavigateToWaypoint__typesupport_c = {
  NULL, NULL, NULL, NULL, NULL,
  &sr_interfaces__action__NavigateToWaypoint__get_type_hash,
  &sr_interfaces__action__NavigateToWaypoint__get_type_description,
  &sr_interfaces__action__NavigateToWaypoint__get_type_description_sources,
};

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_action_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__ACTION_SYMBOL_NAME(
  rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint)()
{
  // Thread-safe by always writing the same values to the static struct
  _sr_interfaces__action__NavigateToWaypoint__typesupport_c.goal_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_SendGoal)();
  _sr_interfaces__action__NavigateToWaypoint__typesupport_c.result_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_GetResult)();
  _sr_interfaces__action__NavigateToWaypoint__typesupport_c.cancel_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, srv, CancelGoal)();
  _sr_interfaces__action__NavigateToWaypoint__typesupport_c.feedback_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, sr_interfaces, action, NavigateToWaypoint_FeedbackMessage)();
  _sr_interfaces__action__NavigateToWaypoint__typesupport_c.status_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, msg, GoalStatusArray)();

  return &_sr_interfaces__action__NavigateToWaypoint__typesupport_c;
}

#ifdef __cplusplus
}
#endif
