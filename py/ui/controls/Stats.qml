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
        
        text: tr("STATS")
    }
    Title {
        Layout.fillWidth: true        
        Layout.margins: 9        
        font.pixelSize: 18
        
        text: tr("STATS_INGAME")
    }
    SettingInt {
        setting: model ? model.p_time_listened : null
        readonly: true
        function captionOperator(val) { return "%1s".arg( parseInt(val/1000) ) }
    }
    Item {
        Layout.fillHeight: true
    }
}
