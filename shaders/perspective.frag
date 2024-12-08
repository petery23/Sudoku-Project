#version 330 core

in vec2 fragmentTexCoord;

out vec4 color;

uniform sampler2D imageTexture;

void main() {
    color = texture(imageTexture, fragmentTexCoord);

    // Smooth edges to reduce aliasing
    color.a *= 1.0f - smoothstep(0.497, 0.5, max(abs(fragmentTexCoord.x - 0.5), abs(fragmentTexCoord.y - 0.5)));
}