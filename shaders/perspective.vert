#version 330 core

layout (location = 0) in vec3 vertexPos;
layout (location = 1) in vec2 vertexTexCoord;

uniform mat4 u_projMat;
uniform mat4 u_viewMat;
uniform mat4 u_modelMat;

out vec2 fragmentTexCoord;

void main()
{
    fragmentTexCoord = vertexTexCoord;
    gl_Position = u_projMat * u_viewMat * u_modelMat * vec4(vertexPos, 1.0);
}