idf_component_register(
    SRCS
        "src/main.c"
        "src/hooks.c"
)

idf_component_set_property(${COMPONENT_NAME} WHOLE_ARCHIVE TRUE)