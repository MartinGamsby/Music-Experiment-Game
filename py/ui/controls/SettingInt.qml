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
    visible: setting ? setting.p_unlocked : false
    property bool readonly: !visible
    
    function captionOperator(val) { return val }
    
    Text {
        text: (setting ? tr(setting.p_name) : "") + (readonly ? ":" : "")
        color: enabled ? Material.foreground : Material.hintTextColor
    }
    Slider {    
        id: slider
        visible: !readonly
        Layout.fillWidth: true
        Layout.fillHeight: false
        Layout.maximumWidth: 200
            
        value: setting ? setting.i : 0
        // TODO: from/to
        from: 0
        to: Math.max(100, setting ? setting.i : 0)
        onMoved: {
            setting.i = value
        }
    }
    Text {
        text: captionOperator(setting ? setting.i : 0)
        color: enabled ? Material.foreground : Material.hintTextColor
    }
}