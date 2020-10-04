import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

Drawer {
    width: parent.width * Consts.DrawerWidthCoefficient
    height: parent.height
    Overlay.modal: Rectangle { color: Consts.ShadowColor }

    ColumnLayout {
        width: parent.width
        height: parent.height
        spacing: Consts.ArtListItemMargin

        ToolBar {
            Material.foreground: parent.Material.foreground
            Material.background: parent.Material.background
            Layout.fillWidth: true
            leftPadding: Consts.ToolbarPadding
            rightPadding: leftPadding
            z: 1

            RowLayout {
                anchors.fill: parent

                Label {
                    Layout.fillWidth: true
                    leftPadding: Consts.ToolbarTitlePadding
                    text: Consts.DrawerTitle
                    font.pixelSize: Consts.DrawerTitleFontSize
                    font.bold: true
                }
                ToolButton {
                    icon.source: Consts.AddImgButtonImgSrc
                    ToolTip.visible: hovered
                    ToolTip.delay: Consts.TooltipDelay
                    ToolTip.text: Consts.AddImgButtonText
                    onClicked: Gui.open_art_dialog(-1)
                }
            }
        }
        ListView {
            id: artList
            objectName: "artList"
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.bottomMargin: Consts.ArtListItemMargin
            spacing: Consts.ArtListItemMargin
            model: ArtFactory

            delegate: ListItem {}
            ScrollIndicator.vertical: ScrollIndicator {}
            add: Transition {
                ParallelAnimation {
                    NumberAnimation {
                        property: "opacity"; from: 0; to: 1.0;
                        duration: Consts.ArtListItemAnimationDuration
                    }
                    NumberAnimation {
                        property: "scale"; from: 0; to: 1.0;
                        duration: Consts.ArtListItemAnimationDuration
                    }
                }
            }
            remove: Transition {
                ParallelAnimation {
                    NumberAnimation {
                        property: "opacity"; to: 0;
                        duration: Consts.ArtListItemAnimationDuration
                    }
                    NumberAnimation {
                        property: "scale"; to: 0;
                        duration: Consts.ArtListItemAnimationDuration
                    }
                }
            }
            displaced: Transition {
                NumberAnimation {
                    properties: "x, y";
                    duration: Consts.ArtListItemAnimationDuration
                }
            }
            removeDisplaced: displaced
        }
    }
}