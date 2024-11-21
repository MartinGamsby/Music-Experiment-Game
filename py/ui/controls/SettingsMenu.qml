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
    SettingBool {
        setting: model ? model.p_generate_mp3 : null
    }
    //SettingInt {
    //    setting: model ? model.p_ideas : null
    //}
    Item {
        Layout.fillHeight: true
    }
}
