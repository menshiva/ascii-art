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
        property string grayscale: ""
        property double animationDuration: Consts.DefaultAnimationDuration
    }
    FontLoader {
        id: modenineFont
        source: Consts.FontSrc
    }

    MainToolbar {
        id: toolbar
        anchors.left: parent.left
        anchors.right: parent.right
    }
    GroupBox {
        anchors.top: toolbar.bottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: Consts.ArtLayoutMargins

        Label {
            id: artLayout
            objectName: "artLayout"
            anchors.fill: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.family: modenineFont.name
            font.pixelSize: Consts.DefaultArtSize
            font.kerning: false
            font.preferShaping: false
            textFormat: Text.PlainText
            clip: true
        }
    }
    SideDrawer { id: drawer }
    ImageDialog { objectName: "imageDialog" }
    SettingsDialog { id: settingsDialog }
}