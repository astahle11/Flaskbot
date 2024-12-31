import json
import uuid

import dearpygui.dearpygui as dpg

input_message = ""
messages = ""

# Default values, can be modified within the application
username = "You"
client_id = str(uuid.uuid4())
topic = "General Chat"

message = {}


def send_message(text):
    message["sender"] = dpg.get_value("username_input")
    message["clientId"] = dpg.get_value("client_id_input")
    message["topic"] = topic
    message["text"] = text

    # Maybe keep this.
    json.dumps(message)

    return


def send_user_message():
    send_message(dpg.get_value("message_input"))

    dpg.set_value("message_input", "")


# The callback for when a PUBLISH message is received from the server.
def on_message(response):
    try:
        dpg.set_value("message_display", response)

    except (ValueError, KeyError):
        print("Malformed data encountered")


# Set last will message
message["sender"] = "AI"
last_will_message_data = json.dumps(message)


# Create the GUI window
dpg.create_context()
dpg.create_viewport(title="AI Chat", width=1000, height=800)


def checkbox_clicked():
    dpg.configure_item("message_display", tracked=dpg.get_value("autoscroll_checkbox"))


with dpg.window(tag="primary_window", width=1000, height=800):
    # Input fields for metadata (username, topic, clientId)
    with dpg.child_window(tag="metadata_inputs", autosize_x=True, height=40):
        with dpg.group(horizontal=True):
            dpg.add_text("Username:")
            dpg.add_input_text(tag="username_input", default_value=username, width=150)

            # Use for conversation title maybe?
            # dpg.add_text("Topic:")
            # dpg.add_input_text(tag="topic_input", default_value=topic, width=150)

            dpg.add_text("Autoscroll:")
            dpg.add_checkbox(tag="autoscroll_checkbox", callback=checkbox_clicked)

    # Message history display
    with dpg.child_window(tag="messages_display", autosize_x=True, height=690):
        dpg.add_text(wrap=750, tag="message_display", tracked=False, track_offset=1.0)
        dpg.add_spacer(height=5)

    # Message input field
    with dpg.child_window(tag="message_inputs", height=40, autosize_x=True):
        with dpg.group(horizontal=True):
            dpg.add_input_text(
                hint="Enter message here...",
                tag="message_input",
                on_enter=True,
                callback=send_user_message,
                width=-100,
            )
            dpg.add_button(label="Send", callback=send_message, width=80)

# demo.show_demo()
# dpg.show_font_manager()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary_window", True)
dpg.start_dearpygui()

dpg.destroy_context()
