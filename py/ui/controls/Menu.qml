import QtQuick
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtQuick.Controls.Material

// For State and MusicState enums
import com.martingamsby.music 1.0

Item {
    id: menuRoot
    implicitWidth: buttons.width
    implicitHeight: buttons.height
    readonly property color backgroundColor: "#222222"
    
    Button {
        id: buttons
        text: "test"
        
        enabled: model ? model.p_music_state_id != MusicStateEnum.GENERATING : false // TODO: Not enough ...
        onClicked: {
            backend.ok_pressed(buttons.text)
        }
    }
}
