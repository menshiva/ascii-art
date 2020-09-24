import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    visible: true
    minimumWidth: 800
    minimumHeight: 600
    title: Consts.MainTitle
    Material.theme: Material.Light
    Material.primary: Material.Teal
    Material.accent: Material.Red

    header: ToolBar {
        leftPadding: 8
        rightPadding: 16
        Material.foreground: "white"

        RowLayout {
            anchors.fill: parent

            ToolButton {
                icon.source: Consts.DrawerButtonImgSrc
                onClicked: drawer.open()
            }
            Label {
                leftPadding: 8
                verticalAlignment: Qt.AlignVCenter
                Layout.fillWidth: true
                text: Consts.MainTitle
                font.pixelSize: 18
            }
            ToolButton {
                enabled: false
                icon.source: Consts.PlayButtonImgSrc
                text: Consts.PlayButtonText
            }
            ToolSeparator {}
            ToolButton {
                enabled: false
                icon.source: Consts.StopButtonImgSrc
                text: Consts.StopButtonText
            }
        }
    }
    GroupBox {
        implicitWidth: parent.width
        implicitHeight: parent.height
        anchors.fill: parent
        anchors.margins: 32
        clip: true

        Label {
            anchors.fill: parent
        }
    }
    Drawer {
        id: drawer
        width: parent.width * 0.32
        height: parent.height

        ColumnLayout {
            width: parent.width
            height: parent.height
            spacing: 0

            RowLayout {
                width: parent.width
                Layout.preferredHeight: 64
                Layout.leftMargin: 16
                Layout.rightMargin: 8

                Label {
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignVCenter
                    text: Consts.DrawerTitle
                    font.pixelSize: 18
                    font.weight: Font.Bold
                }
                RoundButton {
                    Layout.alignment: Qt.AlignVCenter
                    flat: true
                    icon.source: Consts.AddImgButtonImgSrc
                    ToolTip.visible: hovered
                    ToolTip.delay: 100
                    ToolTip.text: Consts.AddImgButtonTooltip
                }
            }
            Divider {}
            // TODO
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignBottom
                color: "white"
            }
        }
    }
}