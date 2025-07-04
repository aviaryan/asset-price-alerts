import subprocess


def show_notification(message, title="Notification", subtitle="", sound_name="default"):
    """
    Display a notification on macOS using AppleScript.
    
    Args:
        message (str): The main notification message
        title (str): The notification title (default: "Notification")
        subtitle (str): The notification subtitle (default: "")
        sound_name (str): The notification sound name (default: "default")
                         Options: "default", "Basso", "Blow", "Bottle", "Frog", "Funk", "Glass", "Hero", "Morse", "Ping", "Pop", "Purr", "Sosumi", "Submarine", "Tink"
                         Use "" for no sound
    
    Returns:
        bool: True if notification was sent successfully, False otherwise
    """
    try:
        # Build AppleScript command with proper syntax
        # Escape double quotes in the strings for AppleScript
        escaped_message = message.replace('"', '\\"')
        escaped_title = title.replace('"', '\\"') if title else ""
        escaped_subtitle = subtitle.replace('"', '\\"') if subtitle else ""
        escaped_sound_name = sound_name.replace('"', '\\"') if sound_name else ""
        
        script = f'display notification "{escaped_message}"'
        
        if title:
            script += f' with title "{escaped_title}"'
        
        if subtitle:
            script += f' subtitle "{escaped_subtitle}"'
        
        if sound_name:
            script += f' sound name "{escaped_sound_name}"'
        
        # Execute the AppleScript command
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return True
        else:
            print(f"AppleScript error (return code {result.returncode}):")
            print(f"stdout: {result.stdout}")
            print(f"stderr: {result.stderr}")
            return False
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError) as e:
        print(f"Error displaying notification: {e}")
        return False


def show_simple_notification(text):
    """
    Display a simple notification with just text.
    
    Args:
        text (str): The notification text to display
    
    Returns:
        bool: True if notification was sent successfully, False otherwise
    """
    return show_notification(text, title="Alert")


if __name__ == "__main__":
    # Example usage
    show_notification("This is a test notification!", "Test Title", "Test Subtitle")
    show_simple_notification("Simple notification example")
