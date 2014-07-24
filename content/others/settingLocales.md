Title: 設定 locale
Tags: ubuntu
Slug: settingLocales
Category: Others
Author: twmht

Regenate all the locales

    :::bash
    sudo dpkg-reconfigure locales

以上會輸出

    :::bash
    Generating locales...
      en_AG.UTF-8... done
      en_AU.UTF-8... done
      en_BW.UTF-8... done
      en_CA.UTF-8... done
      en_DK.UTF-8... done
      en_GB.UTF-8... done
      en_HK.UTF-8... done
      en_IE.UTF-8... done
      en_IN.UTF-8... done
      en_NG.UTF-8... done
      en_NZ.UTF-8... done
      en_PH.UTF-8... done
      en_SG.UTF-8... done
      en_US.UTF-8... up-to-date
      en_ZA.UTF-8... done
      en_ZM.UTF-8... done
      en_ZW.UTF-8... done
    Generation complete.

接著設定系統的 locale

    :::bash
    sudo update-locale LANG=en_US.UTF-8
