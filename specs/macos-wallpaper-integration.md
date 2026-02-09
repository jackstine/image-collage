# macOS Desktop Wallpaper Integration

## Topic of Concern
The macOS desktop wallpaper integration sets the generated image as the system wallpaper.

## Overview
After generating the combined output image, the user can set it as the desktop wallpaper on macOS. This is accomplished via an AppleScript command that tells System Events to update the wallpaper across all desktops.

## Functional Requirements

### Wallpaper Setting
- The wallpaper is set using the macOS `osascript` command-line utility
- The command targets `System Events` to set the picture of **every desktop**
- The image path provided to the command must be an **absolute file path**

### Command Format
- The AppleScript command follows the pattern:
  ```
  osascript -e 'tell application "System Events" to set picture of every desktop to "<absolute_path>"'
  ```

### Path Requirements
- The image path must be a full absolute path (not relative)
- The path points to the generated output image

## Acceptance Criteria
- [ ] An AppleScript command is documented for setting the desktop wallpaper
- [ ] The command sets the wallpaper across all macOS desktops
- [ ] The command requires an absolute file path to the output image
- [ ] The integration uses the `osascript` CLI utility with System Events

## Related Specs
- [[image-rescaling-and-layout|Image Rescaling and Layout]] - Describes how the output image is generated
- [[output-overflow-handling|Output Overflow Handling]] - Describes how the final output file is saved
