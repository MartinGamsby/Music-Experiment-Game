import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Basic
import QtQuick.Controls.Material
import QtQuick.Dialogs

// For State and MusicState enums
import com.martingamsby.music 1.0

ColumnLayout {
    id: settingsMenuRoot
    
    Text {
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        Layout.fillWidth: true
        font.pixelSize: 32
        
        Layout.margins: 9
        
        color: "white"
        text: tr("SETTINGS")
    }
    CheckBox {
        id: cbGenerate
        Layout.fillWidth: true
        Layout.fillHeight: false
            
        text: tr("SETTING_GENERATE_MP3")
        checked: model ? model.p_generate_mp3.b : false
        onClicked: {
            model.p_generate_mp3.b = checked
        }
        enabled: model ? model.p_generate_mp3.p_locked : false
    }
    Item {
        Layout.fillHeight: true
    }
}
