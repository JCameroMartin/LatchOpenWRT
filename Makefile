include $(TOPDIR)/rules.mk

PKG_NAME:=LatchOpenWRT
PKG_VERSION:=1.0.0
PKG_RELEASE:=1
PKG_MAINTAINER:=Juan Camero
PKG_LICENSE:=LGPL-2.1
PKG_CONFIG_DEPENDS:=luasql-sqlite3 ca-certificates python-light python-codecs python-sqlite3 python-logging python-openssl
include $(INCLUDE_DIR)/package.mk

PKG_BUILD_DIR := $(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

define Package/LatchOpenWRT
  SECTION:=utils
  CATEGORY:=Utilities
  DEPENDS:=+luasql-sqlite3 +ca-certificates +python-light +python-codecs +python-sqlite3 +python-logging +python-openssl
  TITLE:=Latch plugin to control Wi-Fi access
  URL:=https://github.com/JCameroMartin/LatchOpenWRT
  MENU:=1
endef

define Package/LatchOpenWRT/description
 Plugin to integrate Latch technology from Telefonica with OpenWRT for allow or block the access to the network of devices through Wi-Fi
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) ./src/* $(PKG_BUILD_DIR)/
endef

define Build/Compile
endef

define Package/LatchOpenWRT/install
	$(INSTALL_DIR) $(1)/root/Latch
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/Latch/* $(1)/root/Latch/
	$(INSTALL_DIR) $(1)/usr/lib/lua/luci/controller/Latch
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/controller/Latch/* $(1)/usr/lib/lua/luci/controller/Latch/
	$(INSTALL_DIR) $(1)/usr/lib/lua/luci/view/Latch
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/view/Latch/* $(1)/usr/lib/lua/luci/view/Latch/
	$(INSTALL_DIR) $(1)/www
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/www/* $(1)/www/
	$(INSTALL_DIR) $(1)/www/images
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/images/* $(1)/www/images/
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/initd/* $(1)/etc/init.d/
endef

$(eval $(call BuildPackage,LatchOpenWRT))	
