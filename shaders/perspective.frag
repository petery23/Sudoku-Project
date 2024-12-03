#version 330 core

in vec2 uv;
flat in vec2 o;
in vec3 p;

uniform bool cull_back = false;

out vec4 color;

uniform sampler2D imageTexture;

void main() {
    if (cull_back && p.z <= 0.0) discard;
    vec2 uv = (p.xy / p.z).xy - o;
    color = texture(imageTexture, uv + 0.5);
    color.a *= step(max(abs(uv.x), abs(uv.y)), 0.5);
}