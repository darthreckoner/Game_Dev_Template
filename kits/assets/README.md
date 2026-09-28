# Asset service configuration

Enable a service only after the user approves it in the Project settings of
`DESIGN.md` (tool budget). The Director (Claude) uses these for art; the coder
does not need them.

## Claude Code

Copy the entries you need from `mcp.example.json` into the project's `.mcp.json`.
Set the keys as user environment variables; never commit key values. Claude Code
expands `${VAR}` in `.mcp.json`.

The PixelLab entry follows PixelLab's published configuration (remote HTTP server
with a bearer token). For other services, copy the current configuration from the
vendor's official README at install time and verify it with one small request:

- ElevenLabs: <https://github.com/elevenlabs/elevenlabs-mcp>
- Tripo: <https://github.com/vast-ai-research/tripo-mcp>
- Meshy: <https://github.com/meshy-dev/meshy-mcp-server>
- Retro Diffusion: hosted MCP; see <https://retrodiffusion.ai/>

After enabling a service, record the plan tier and its commercial terms in the
Project settings of `DESIGN.md`, and log every generated asset in
`assets/ASSET_SOURCES.md`.
