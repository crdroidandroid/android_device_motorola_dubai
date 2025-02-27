#
# SPDX-FileCopyrightText: 2022-2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

DEVICE_PATH := device/motorola/dubai

# Inherit from motorola sm7325-common
include device/motorola/sm7325-common/BoardConfigCommon.mk

# Audio (Dolby)
AUDIO_FEATURE_ENABLED_DS2_DOLBY_DAP := true

# Bootloader
TARGET_BOOTLOADER_BOARD_NAME := dubai

# Fingerprint
TARGET_SURFACEFLINGER_UDFPS_LIB := //$(DEVICE_PATH):libudfps_extension.dubai
SOONG_CONFIG_qtidisplay_udfps := true

# HIDL
DEVICE_FRAMEWORK_COMPATIBILITY_MATRIX_FILE += $(DEVICE_PATH)/device_framework_matrix.xml
DEVICE_MANIFEST_FILE += $(DEVICE_PATH)/manifest.xml

# Kernel
BOARD_KERNEL_CMDLINE += androidboot.hab.product=dubai
TARGET_KERNEL_CONFIG += vendor/lineage_dubai.config

# Kernel Modules
BOARD_VENDOR_KERNEL_MODULES_LOAD := $(strip $(shell cat $(DEVICE_PATH)/modules.load))
BOARD_VENDOR_KERNEL_MODULES_BLOCKLIST_FILE := $(DEVICE_PATH)/modules.blocklist
BOARD_VENDOR_RAMDISK_RECOVERY_KERNEL_MODULES_LOAD := $(strip $(shell cat $(DEVICE_PATH)/modules.load.recovery))
BOOT_KERNEL_MODULES := $(BOARD_VENDOR_RAMDISK_RECOVERY_KERNEL_MODULES_LOAD)

# Partitions
BOARD_USERDATAIMAGE_PARTITION_SIZE := 116340535296
BOARD_MOT_DP_GROUP_SIZE := 8921284608 # ( BOARD_SUPER_PARTITION_SIZE - 4MB )
BOARD_SUPER_PARTITION_SIZE := 8925478912

# Properties
TARGET_PRODUCT_PROP += $(DEVICE_PATH)/product.prop
TARGET_SYSTEM_PROP += $(DEVICE_PATH)/system.prop
TARGET_VENDOR_PROP += $(DEVICE_PATH)/vendor.prop

# Recovery
TARGET_RECOVERY_UI_MARGIN_HEIGHT := 90

# Security
BOOT_SECURITY_PATCH := 2025-01-01
VENDOR_SECURITY_PATCH := $(BOOT_SECURITY_PATCH)

# Verified Boot
BOARD_AVB_ROLLBACK_INDEX := 27
BOARD_AVB_VBMETA_SYSTEM_ROLLBACK_INDEX := 27

# inherit from the proprietary version
include vendor/motorola/dubai/BoardConfigVendor.mk
include hardware/motorola/dolby/BoardConfigVendor.mk