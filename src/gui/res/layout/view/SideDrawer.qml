import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

Drawer {
    width: Consts.DrawerWidth
    height: parent.height
    Overlay.modal: Rectangle {
        color: Consts.ShadowColor
    }

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
                    leftPadding: Consts.ToolbarTitlePadding
                    Layout.fillWidth: true
                    text: Consts.DrawerTitle
                    font.pixelSize: Consts.DrawerTitleFontSize
                    font.weight: Font.Bold
                }
                ToolButton {
                    objectName: "addImageBtn"
                    icon.source: Consts.AddImgButtonImgSrc
                    ToolTip.visible: hovered
                    ToolTip.delay: Consts.TooltipDelay
                    ToolTip.text: Consts.AddImgButtonTooltip
                    //onClicked: drawer.close()  TODO
                }
            }
        }
        ListView {
            id: artList
            objectName: "artList"
            Layout.fillWidth: true
            Layout.fillHeight: true
            leftMargin: Consts.ArtListItemMargin
            rightMargin: leftMargin
            spacing: leftMargin
            model: ArtModels

            delegate: ListItem {}
            ScrollIndicator.vertical: ScrollIndicator {}
            add: Transition {
                ParallelAnimation {
                    NumberAnimation {
                        property: "opacity"; from: 0; to: 1.0; duration: Consts.ArtListItemAnimationDuration
                    }
                    NumberAnimation {
                        property: "scale"; from: 0; to: 1.0; duration: Consts.ArtListItemAnimationDuration
                    }
                }
            }
            remove: Transition {
                ParallelAnimation {
                    NumberAnimation {
                        property: "opacity"; to: 0; duration: Consts.ArtListItemAnimationDuration
                    }
                    NumberAnimation {
                        property: "scale"; to: 0; duration: Consts.ArtListItemAnimationDuration
                    }
                }
            }
            displaced: Transition {
                NumberAnimation {
                    properties: "x,y"; duration: Consts.ArtListItemAnimationDuration
                }
            }
            removeDisplaced: displaced
        }
    }
}