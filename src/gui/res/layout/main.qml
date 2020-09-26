import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import Qt.labs.settings 1.0
import "view"

ApplicationWindow {
    id: window
    Material.theme: Material[Consts.SettingsThemeModels[settings.theme]]
    Material.primary: Material.Teal
    Material.accent: Material.primary
    minimumWidth: Consts.ApplicationMinWidth
    minimumHeight: Consts.ApplicationMinHeight
    title: Consts.ToolbarTitle
    visible: true

    Settings {
        id: settings
        objectName: "settings"
        property alias width: window.width
        property alias height: window.height
        property int theme: 0
        property string grayscale: ""  // TODO
    }

    header: MainToolbar {}
    GroupBox {
        anchors.fill: parent
        anchors.margins: Consts.ArtLayoutMargins

        Label {
            objectName: "artLayout"
            anchors.fill: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }
    SideDrawer {
        id: drawer
    }
    SettingsDialog {
        id: settingsDialog
    }
}