 for i in reversed(range(layout.count())):
            widget_to_remove = layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()
                layout.removeWidget(widget_to_remove)
        