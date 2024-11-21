import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Basic
import QtQuick.Controls.Material
import QtQuick.Dialogs

// For State and MusicState enums
import com.martingamsby.music 1.0

RowLayout {
    required property Setting setting
    implicitWidth: slider.implicitWidth
    Layout.margins: 9
    enabled: setting ? setting.p_unlocked : false
    
    Text {
        text: setting ? tr(setting.p_name) : ""
        color: "white"
    }
    Slider {    
        id: slider
        Layout.fillWidth: true
        Layout.fillHeight: false
        Layout.maximumWidth: 200
            
        value: setting ? setting.i : 0
        // TODO: from/to
        from: 0
        to: 100
        onMoved: {
            setting.i = value
        }
    }
}