import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    Material.theme: Material.Light
    Material.primary: Material.Teal
    Material.accent: Material.Red
    minimumWidth: Consts.ApplicationMinWidth
    minimumHeight: Consts.ApplicationMinHeight
    title: Consts.ToolbarTitle
    visible: true

    header: ToolBar {
        Material.foreground: "white"
        leftPadding: Consts.ToolbarPadding
        rightPadding: Consts.ToolbarPadding

        RowLayout {
            anchors.fill: parent

            ToolButton {
                icon.source: Consts.DrawerButtonImgSrc
                onClicked: drawer.open()
            }
            Label {
                leftPadding: Consts.ToolbarTitlePadding
                rightPadding: Consts.ToolbarTitlePadding
                verticalAlignment: Qt.AlignVCenter
                Layout.fillWidth: true
                text: Consts.ToolbarTitle
                font.pixelSize: Consts.ToolbarTitleFontSize
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
        anchors.margins: Consts.ArtLayoutMargins
        clip: true

        Label {
            objectName: "artLayout"
            anchors.fill: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }
    Drawer {
        id: drawer
        width: parent.width * Consts.DrawerWidthCoefficient
        height: parent.height

        ColumnLayout {
            width: parent.width
            height: parent.height
            spacing: 0

            RowLayout {
                width: parent.width
                Layout.preferredHeight: Consts.DrawerTitleHeight
                Layout.leftMargin: Consts.DrawerTitleLeftMargin
                Layout.rightMargin: Consts.DrawerTitleRightMargin

                Label {
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignVCenter
                    text: Consts.DrawerTitle
                    font.pixelSize: Consts.DrawerTitleFontSize
                    font.weight: Font.Bold
                }
                RoundButton {
                    Layout.alignment: Qt.AlignVCenter
                    flat: true
                    icon.source: Consts.AddImgButtonImgSrc
                    ToolTip.visible: hovered
                    ToolTip.delay: Consts.DrawerButtonTooltipDelay
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