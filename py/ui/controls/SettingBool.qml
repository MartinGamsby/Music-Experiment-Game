import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Basic
import QtQuick.Controls.Material
import QtQuick.Dialogs

// For State and MusicState enums
import com.martingamsby.music 1.0

CheckBox {    
    required property Setting setting
    
    Layout.fillWidth: true
    Layout.fillHeight: false
        
    text: setting ? tr(setting.p_name) : ""
    checked: setting ? setting.b : false
    onClicked: {
        setting.b = checked
    }
    enabled: setting ? setting.p_unlocked : false
}