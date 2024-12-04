#version 330 core
precision highp float;

layout (location = 0) in vec3 vertexPos;
layout (location = 1) in vec2 vertexTexCoord;

flat out vec2 o;
out vec3 p;

// All in degrees
uniform float fov = 30.0f;
uniform float y_rot = 0.0f;
uniform float x_rot = 0.0f;
const float inset = -500.0f;
// Consider changing this to a uniform and changing it from code

uniform float texturePixelSize;

const float PI = 3.14159;

void main()
{
    float sin_b = sin(y_rot / 180.0 * PI);
    float cos_b = cos(y_rot / 180.0 * PI);
    float sin_c = sin(x_rot / 180.0 * PI);
    float cos_c = cos(x_rot / 180.0 * PI);

    mat3 inv_rot_mat;
    inv_rot_mat[0][0] = cos_b;
    inv_rot_mat[0][1] = 0.0;
    inv_rot_mat[0][2] = -sin_b;

    inv_rot_mat[1][0] = sin_b * sin_c;
    inv_rot_mat[1][1] = cos_c;
    inv_rot_mat[1][2] = cos_b * sin_c;

    inv_rot_mat[2][0] = sin_b * cos_c;
    inv_rot_mat[2][1] = -sin_c;
    inv_rot_mat[2][2] = cos_b * cos_c;

    float t = tan(fov / 360.0 * PI);
    p = inv_rot_mat * vec3((vertexTexCoord - 0.5), 0.5 / t);
    float v = (0.5 / t) + 0.5;
    p.xy *= v * inv_rot_mat[2].z;
    o = v * inv_rot_mat[2].xy;

    gl_Position = vec4(vertexPos.xy + (vertexTexCoord - 0.5) / texturePixelSize * t * (1.0 - inset), vertexPos.z, 1.0);
}