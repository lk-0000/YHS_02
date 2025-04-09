{pkgs}: {
  deps = [
    pkgs.mailutils
    pkgs.glibcLocales
    pkgs.postgresql
    pkgs.openssl
  ];
}
