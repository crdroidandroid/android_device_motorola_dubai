#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.misc import execute
from extract_utils.extract import extract_fns_user_type
from extract_utils.extract_star import extract_star_firmware
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'vendor/motorola/sm7325-common',
    'hardware/qcom-caf/sm8350',
    'hardware/qcom-caf/wlan',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
}

blob_fixups: blob_fixups_user_type = {
    'product/priv-app/MotCamera4/MotCamera4.apk': blob_fixup()
        .apktool_patch('MotCamera4-patches'),
    ('vendor/lib/libmot_chi_desktop_helper.so', 'vendor/lib64/libmot_chi_desktop_helper.so'): blob_fixup()
        .add_needed('libgui_shim_vendor.so'),
}  # fmt: skip

extract_fns: extract_fns_user_type = {
    r'(bootloader|radio)\.img': extract_star_firmware,
}

# Dolby fixups
dolby_fixups = [
    execute(f"{PATCHELF} --replace-needed \"libstagefright_foundation.so\" \"libstagefright_foundation-v33.so\" \"{DEVICE_BLOB_ROOT}/vendor/lib/libstagefright_soft_ddpdec.so\""),
    execute(f"{PATCHELF} --replace-needed \"libstagefright_foundation.so\" \"libstagefright_foundation-v33.so\" \"{DEVICE_BLOB_ROOT}/vendor/lib/libstagefright_soft_ac4dec.so\""),
    execute(f"{PATCHELF} --replace-needed \"libstagefright_foundation.so\" \"libstagefright_foundation-v33.so\" \"{DEVICE_BLOB_ROOT}/vendor/lib/libstagefrightdolby.so\""),
    execute(f"{PATCHELF} --replace-needed \"libstagefright_foundation.so\" \"libstagefright_foundation-v33.so\" \"{DEVICE_BLOB_ROOT}/vendor/lib64/libstagefright_soft_ddpdec.so\""),
    execute(f"{PATCHELF} --replace-needed \"libstagefright_foundation.so\" \"libstagefright_foundation-v33.so\" \"{DEVICE_BLOB_ROOT}/vendor/lib64/libdlbdsservice.so\""),
    execute(f"{PATCHELF} --replace-needed \"libstagefright_foundation.so\" \"libstagefright_foundation-v33.so\" \"{DEVICE_BLOB_ROOT}/vendor/lib64/libstagefright_soft_ac4dec.so\""),
    execute(f"{PATCHELF} --replace-needed \"libstagefright_foundation.so\" \"libstagefright_foundation-v33.so\" \"{DEVICE_BLOB_ROOT}/vendor/lib64/libstagefrightdolby.so\""),
]

# Add Dolby fixups to blob_fixups dictionary
blob_fixups.update({f"dolby_fixup_{i}": fixup for i, fixup in enumerate(dolby_fixups)})

module = ExtractUtilsModule(
    'dubai',
    'motorola',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    extract_fns=extract_fns,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'sm7325-common', module.vendor
    )
    utils.run()
