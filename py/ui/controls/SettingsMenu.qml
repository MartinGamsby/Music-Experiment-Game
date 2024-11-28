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
    
    Title {
        Layout.fillWidth: true
        
        Layout.margins: 9
        
        color: enabled ? Material.foreground : Material.hintTextColor
        text: tr("SETTINGS")
    }
    SettingBool {
        setting: model ? model.p_fullscreen : null
    }
    SettingBool {
        setting: model ? model.p_autoload : null
    }
    SettingBool {
        setting: model ? model.p_generate_mp3 : null
    }
    SettingBool {
        setting: model ? model.p_gui_playback : null
    }
    //SettingInt {
    //    setting: model ? model.p_ideas : null
    //}
    Item {
        Layout.fillHeight: true
    }
}
