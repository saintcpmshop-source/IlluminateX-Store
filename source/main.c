/* 
 * IlluminateStore - PS3 In-Console App Store
 * Copyright (c) 2026 saintcpmshop-source. All Rights Reserved.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sysutil/sysutil.h>
#include <sys/process.h>
#include <sys/timer.h>
#include <net/net.h>
#include <net/http.h>

// The raw link to your manifest on GitHub
#define MANIFEST_URL "https://raw.githubusercontent.com/saintcpmshop-source/IlluminateStore/main/manifest.json"

void download_pkg(const char* url, const char* pkg_name) {
    char dest[256];
    snprintf(dest, sizeof(dest), "/dev_hdd0/tmp/%s", pkg_name);
    
    printf("\n[!] Downloading: %s\n", pkg_name);
    printf("[!] URL: %s\n", url);
    
    // PSL1GHT HTTP download function goes here
    // http_download(url, dest);
    
    printf("[+] Download complete! Go to Package Manager to install.\n");
}

int main(int argc, char *argv[]) {
    sysUtilInit();
    
    printf("==========================================\n");
    printf("       IlluminateStore - App Hub          \n");
    printf("==========================================\n\n");
    
    printf("[!] Fetching App List from GitHub...\n");
    
    // In a real build, it downloads MANIFEST_URL and parses the JSON here.
    // For now, it lists the apps matching the manifest above.
    
    printf("\nAvailable Apps:\n");
    printf("1. IlluminateMount\n");
    printf("2. webMAN MOD\n");
    printf("3. Apollo Save Tool\n\n");

    printf("Select a number to download (1-3): ");
    
    int choice;
    if (scanf("%d", &choice) == 1) {
        if (choice == 1) {
            download_pkg("https://github.com/saintcpmshop-source/IlluminateX-PKGs/releases/latest/download/IlluminateMount.pkg", "IlluminateMount.pkg");
        } else if (choice == 2) {
            download_pkg("https://github.com/aldostools/webMAN-MOD/releases/latest/download/webMAN_MOD_Installer.pkg", "webMAN.pkg");
        } else if (choice == 3) {
            download_pkg("https://github.com/bucanero/apollo-ps3/releases/latest/download/apollo-ps3.pkg", "Apollo.pkg");
        }
    }

    printf("\nPress the PS button to exit.\n");
    while(1) {
        sysUtilCheckCallback(); 
        sysUtilSleep(100); 
    }

    sysUtilExit();
    return 0;
}
