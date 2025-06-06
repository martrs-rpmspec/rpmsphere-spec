Name:           libressl
Version:        4.0.0
Release:        1
Summary:        An SSL/TLS protocol implementation
License:        OpenSSL
Group:          Development/Libraries/C and C++
URL:            https://libressl.org/
#Freshcode-URL: https://freshcode.club/projects/libressl
#Git-Clone:     git://github.com/libressl-portable/portable
#See-Also:      git://github.com/libressl-portable/openbsd
Source:         https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/%name-%version.tar.gz
#Source2:        https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/%name-%version.tar.gz.asc
Source3:        %name.keyring
#Source4:        baselibs.conf-%name
Patch1:         des-fcrypt.diff
Patch2:         extra-symver.diff
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkg-config
Obsoletes:      ssl
Provides:       ssl
#Provides:       openssl(cli)

%description
LibreSSL is an open-source implementation of the Secure Sockets Layer
(SSL) and Transport Layer Security (TLS) protocols. It derives from
OpenSSL, with the aim of refactoring the OpenSSL code so as to
provide a more secure implementation.

%package -n libcrypto45
Summary:        An SSL/TLS protocol implementation
Group:          System/Libraries

%description -n libcrypto45
The "crypto" library implements a wide range of cryptographic
algorithms used in various Internet standards. The services provided
by this library are used by the LibreSSL implementations of SSL, TLS
and S/MIME, and they have also been used to implement SSH, OpenPGP,
and other cryptographic standards.

%package -n libssl47
Summary:        An SSL/TLS protocol implementation
Group:          System/Libraries

%description -n libssl47
LibreSSL is an open-source implementation of the Secure Sockets Layer
(SSL) and Transport Layer Security (TLS) protocols. It derives from
OpenSSL and intends to provide a more secure implementation.

%package -n libtls19
Summary:        A simplified interface for the OpenSSL/LibreSSL TLS protocol implementation
Group:          System/Libraries

%description -n libtls19
LibreSSL is an open-source implementation of the Secure Sockets Layer
(SSL) and Transport Layer Security (TLS) protocols. It derives from
OpenSSL and intends to provide a more secure implementation.

The libtls library provides a modern and simplified interface (of
libssl) for secure client and server communications.

%package devel
Summary:        Development files for LibreSSL, an SSL/TLS protocol implementation
Group:          Development/Libraries/C and C++
Requires:       libcrypto45 = %version
Requires:       libssl47 = %version
Requires:       libtls19 = %version
Conflicts:      libopenssl-devel
Conflicts:      otherproviders(ssl-devel)

%description devel
LibreSSL is an open-source implementation of the Secure Sockets Layer
(SSL) and Transport Layer Security (TLS) protocols. It derives from
OpenSSL, with the aim of refactoring the OpenSSL code so as to
provide a more secure implementation.

This subpackage contains libraries and header files for developing
applications that want to make use of libressl.

%package devel-doc
Summary:        Documentation for the LibreSSL API
Group:          Documentation/Man
BuildArch:      noarch
Conflicts:      openssl-doc

%description devel-doc
LibreSSL is an open-source implementation of the Secure Sockets Layer
(SSL) and Transport Layer Security (TLS) protocols.

This subpackage contains the manpages to the LibreSSL API.

%prep
%setup -q
#patch 1 -p1
#patch 2 -p1

%build
autoreconf -fi
# Some smart people broke disable-static
%configure --enable-libtls
make %{?_smp_mflags}

%install
b="%buildroot"
%make_install
rm -f "$b/%_libdir"/*.la
for i in "$b/%_mandir"/man*; do
        pushd "$i"
        for j in *.*; do
                mv "$j" "${j}ssl"
        done
        popd
done
rm -f "%buildroot/%_sysconfdir/ssl/cert.pem"
rm -f "%buildroot/%_libdir"/*.a
rm -f "%buildroot/%_libdir"/*.la

%post   -n libcrypto45 -p /sbin/ldconfig
%postun -n libcrypto45 -p /sbin/ldconfig
%post   -n libssl47 -p /sbin/ldconfig
%postun -n libssl47 -p /sbin/ldconfig
%post   -n libtls19 -p /sbin/ldconfig
%postun -n libtls19 -p /sbin/ldconfig

%files
%dir %_sysconfdir/ssl/
%config %_sysconfdir/ssl/openssl.cnf
%config %_sysconfdir/ssl/x509v3.cnf
%_bindir/ocspcheck
%_bindir/openssl
%_mandir/man1/*.1*
%_mandir/man5/*.5*
%_mandir/man8/*.8*
%doc COPYING

%files -n libcrypto45
%_libdir/libcrypto.so.*

%files -n libssl47
%_libdir/libssl.so.*

%files -n libtls19
%_libdir/libtls.so.*

%files devel
%_includedir/openssl/
%_includedir/tls.h
%_libdir/libcrypto.so
%_libdir/libssl.so
%_libdir/libtls.so
%_libdir/pkgconfig/*.pc

%files devel-doc
%_mandir/man3/*.*

%changelog
* Sun Dec 8 2024 Wei-Lun Chao <bluebat@member.fsf.org> - 4.0.0
- Rebuilt for Fedora
* Wed May 22 2019 Jan Engelhardt <jengelh@inai.de>
- Update to new upstream release 2.9.2
  * Fixed SRTP profile advertisement for DTLS servers.
* Tue Apr 23 2019 Jan Engelhardt <jengelh@inai.de>
- Update to new upstream release 2.9.1
  * Added the SM4 block cipher from the Chinese standard GB/T
    32907-2016.
  * Partial port of the OpenSSL EC_KEY_METHOD API for use by
    OpenSSH.
  * Implemented further missing OpenSSL 1.1 API.
  * Added support for XChaCha20 and XChaCha20-Poly1305.
  * Added support for AES key wrap constructions via the EVP
    interface.
* Sun Mar 31 2019 Jan Engelhardt <jengelh@inai.de>
- Add openssl(cli) provides. Replace otherproviders conflict
  by normal Conflict+Provides.
* Thu Mar 14 2019 Jan Engelhardt <jengelh@inai.de>
- Update to new upstream release 2.9.0
  * CRYPTO_LOCK is now automatically initialized, with the legacy
    callbacks stubbed for compatibility.
  * Added the SM3 hash function from the Chinese standard GB/T
    32905-2016.
  * Added more OPENSSL_NO_* macros for compatibility with
    OpenSSL.
  * Added the ability to use the RSA PSS algorithm for handshake
    signatures.
  * Added functionality to derive early, handshake, and
    application secrets as per RFC8446.
  * Added handshake state machine from RFC8446.
  * Added support for assembly optimizations on 32-bit ARM ELF
    targets.
  * Improved protection against timing side channels in ECDSA
    signature generation.
  * Coordinate blinding was added to some elliptic curves. This
    is the last bit of the work by Brumley et al. to protect
    against the Portsmash vulnerability.
* Mon Dec 24 2018 sean@suspend.net
- Update to new upstream release 2.8.3
  * Fixed warnings about clock_gettime on Windows VS builds
  * Fixed CMake builds on systems where getpagesize is inline
  * Implemented coordinate blinding for EC_POINT for portsmash
  * Fixed a non-uniformity in getentropy(2) to discard zeroes
* Tue Oct 23 2018 Bernhard Wiedemann <bwiedemann@suse.com>
- Update extra-symver.diff to fix build with -j1
* Fri Oct 19 2018 Jan Engelhardt <jengelh@inai.de>
- Update to new upstream release 2.8.2
  * Added Wycheproof support for ECDH and ECDSA Web Crypto test
    vectors, along with test harness fixes.
* Sat Oct 13 2018 Jan Engelhardt <jengelh@inai.de>
- Update to new upstream release 2.8.1
  * Simplified key exchange signature generation and verification.
  * Fixed a one-byte buffer overrun in callers of
  EVP_read_pw_string.
  * Modified signature of CRYPTO_mem_leaks_* to return -1. This
  function is a no-op in LibreSSL, so this function returns an
  error to not indicate the (non-)existence of memory leaks.
  * SSL_copy_session_id, PEM_Sign, EVP_EncodeUpdate,
  BIO_set_cipher, X509_OBJECT_up_ref_count now return an int for
  error handling, matching OpenSSL.
  * Converted a number of #defines into proper functions, matching
  OpenSSL's ABI.
  * Added X509_get0_serialNumber from OpenSSL.
  * Removed EVP_PKEY2PKCS8_broken and PKCS8_set_broken, while
  adding PKCS8_pkey_add1_attr_by_NID and PKCS8_pkey_get0_attrs,
  matching OpenSSL.
  * Added RSA_meth_get_finish() RSA_meth_set1_name() from OpenSSL.
  * Added new EVP_CIPHER_CTX_(get|set)_iv() API that allows the IV
  to be retrieved and set with appropriate validation.
* Wed Aug  8 2018 jengelh@inai.de
- Update to new upstream release 2.8.0
  * Fixed a pair of 20+ year-old bugs in X509_NAME_add_entry.
  * Tighten up checks for various X509_VERIFY_PARAM functions,
    'poisoning' parameters so that an unverified certificate
    cannot be used if it fails verification.
  * Fixed a potential memory leak on failure in ASN1_item_digest.
  * Fixed a potential memory alignment crash in
    asn1_item_combine_free.
  * Removed unused SSL3_FLAGS_DELAY_CLIENT_FINISHED and
    SSL3_FLAGS_POP_BUFFER flags in write path, simplifying IO
    paths.
  * Removed SSL_OP_TLS_ROLLBACK_BUG buggy client workarounds.
  * Added const annotations to many existing APIs from OpenSSL,
    making interoperability easier for downstream applications.
  * Added a missing bounds check in c2i_ASN1_BIT_STRING.
  * Removed three remaining single DES cipher suites.
  * Fixed a potential leak/incorrect return value in DSA
    signature generation.
  * Added a blinding value when generating DSA and ECDSA
    signatures, in order to reduce the possibility of a
    side-channel attack leaking the private key.
  * Added ECC constant time scalar multiplication support.
  * Revised the implementation of RSASSA-PKCS1-v1_5 to match the
    specification in RFC 8017.
  * Changes from 2.7.4:
  * Avoid a timing side-channel leak when generating DSA and ECDSA
    signatures. [CVE-2018-12434, boo#1097779]
  * Reject excessively large primes in DH key generation.
* Mon May  7 2018 jengelh@inai.de
- Update to new upstream release 2.7.3
  * Removed incorrect NULL checks in DH_set0_key().
  * Limited tls_config_clear_keys() to only clear private keys.
* Mon Apr  2 2018 jengelh@inai.de
- Update to new upstream release 2.7.2
  * Updated and added extensive new HISTORY sections to
    the API manuals.
* Mon Mar 26 2018 jengelh@inai.de
- Update to new upstream release 2.7.1
  * Fixed a bug in int_x509_param_set_hosts, calling strlen() if
    name length provided is 0 to match the OpenSSL behaviour.
    [CVE-2018-8970, boo#1086778]
* Fri Mar 23 2018 jengelh@inai.de
- Update to new upstream release 2.7.0
  * Added support for many OpenSSL 1.0.2 and 1.1 APIs.
  * Added support for automatic library initialization in
    libcrypto, libssl, and libtls.
  * Converted more packet handling methods to CBB, which improves
    resiliency when generating TLS messages.
  * Completed TLS extension handling rewrite, improving consistency
    of checks for malformed and duplicate extensions.
  * Rewrote ASN1_TYPE_ get,set _octetstring() using templated
    ASN.1. This removes the last remaining use of the old M_ASN1_
    macros (asn1_mac.h) from API that needs to continue to exist.
  * Added support for client-side session resumption in libtls.
  * A libtls client can specify a session file descriptor (a
    regular file with appropriate ownership and permissions) and
    libtls will manage reading and writing of session data across
    TLS handshakes.
  * Merged more DTLS support into the regular TLS code path.
* Thu Dec 21 2017 jengelh@inai.de
- Update to new upstream release 2.6.4
  * Make tls_config_parse_protocols() work correctly when passed
    a NULL pointer for a protocol string.
  * Correct TLS extensions handling when no extensions are
    present.
* Mon Dec  4 2017 jengelh@inai.de
- Add extra-symver.diff
* Tue Nov  7 2017 jengelh@inai.de
- Update to new upstream release 2.6.3
  * Added support for providing CRLs to libtls - once a CRL is
    provided via tls_config_set_crl_file(3) or
    tls_config_set_crl_mem(3), CRL checking is enabled and
    required for the full certificate chain.
  * Reworked TLS certificate name verification code to more
    strictly follow RFC 6125.
  * Relaxed SNI validation to allow non-RFC-compliant clients
    using literal IP addresses with SNI to connect to a
    libtls-based TLS server.
  * Added tls_peer_cert_chain_pem() to libtls, useful in private
    certificate validation callbacks such as those in relayd.
  * Added SSL{,_CTX}_set_{min,max}_proto_version(3) functions.
  * Imported HKDF (HMAC Key Derivation Function) from BoringSSL.
  * Dropped cipher suites using DSS authentication.
  * Removed support for DSS/DSA from libssl.
  * Distinguish between self-issued certificates and self-signed
    certificates. The certificate verification code has special
    cases for self-signed certificates and without this change,
    self-issued certificates (which it seems are common place
    with openvpn/easyrsa) were also being included in this
    category.
  * Removed NPN support - NPN was never standardised and the last
    draft expired in October 2012.
  * Removed SSL_OP_CRYPTOPRO_TLSEXT_BUG workaround for old/broken
    CryptoPro clients.
  * Removed support for the TLS padding extension, which was
    added as a workaround for an old bug in F5's TLS termination.
  * Added ability to clamp notafter values in certificates for
    systems with 32-bit time_t. This is necessary to conform to
    RFC 5280 §4.1.2.5.
  * Removed the original (pre-IETF) chacha20-poly1305 cipher
    suites.
  * Reclassified ECDHE-RSA-DES-CBC3-SHA from HIGH to MEDIUM.
- Add des-fcrypt.diff [boo#1065363]
* Mon Oct  2 2017 jengelh@inai.de
- Update to new upstream release 2.6.2
  * Provide a useful error with libtls if there are no OCSP URLs
    in a peer certificate.
  * Keep track of which keypair is in use by a TLS context,
    fixing a bug where a TLS server with SNI would only return
    the OCSP staple for the default keypair.
- Update to new upstream release 2.6.1
  * Added tls_config_set_ecdhecurves() to libtls, which allows
    the names of the eliptical curves that may be used during
    client and server key exchange to be specified.
  * Removed support for DSS/DSA, since we removed the cipher
    suites a while back.
  * Removed NPN support. NPN was never standardised and the last
    draft expired in October 2012. ALPN was standardised.
  * Removed SSL_OP_CRYPTOPRO_TLSEXT_BUG workaround for old/broken
    CryptoPro clients.
  * Removed support for the TLS padding extension, which was
    added as a workaround for an old bug in F5's TLS
    termintation.
  * Added ability to clamp notafter values in certificates for
    systems with 32-bit time_t. This is necessary to conform to
    RFC 5280 §4.1.2.5.
  * Implemented the SSL_CTX_set_min_proto_version(3) API.
  * Removed the original (pre-IETF) chacha20-poly1305 cipher
    suites.
  * Reclassified ECDHE-RSA-DES-CBC3-SHA from HIGH to MEDIUM.
* Fri Sep  1 2017 jengelh@inai.de
- Update to new upstream release 2.6.0
  * Added support for providing CRLs to libtls. Once a CRL is
    provided, we enable CRL checking for the full certificate
    chain.
  * Allow non-compliant clients using IP literal addresses with
    SNI to connect to a server using libtls.
  * Avoid a potential NULL pointer dereference in
    d2i_ECPrivateKey().
  * Added definitions for three OIDs used in EV certificates.
  * Plugged a memory leak in tls_ocsp_free.
  * Added tls_peer_cert_chain_pem, tls_cert_hash, and
    tls_hex_string to libtls, useful in private certificate
    validation callbacks.
  * Reworked TLS certificate name verification code to more
    strictly follow RFC 6125.
  * Added tls_keypair_clear_key for clearing key material.
  * Removed inconsistent IPv6 handling from
    BIO_get_accept_socket, simplified BIO_get_host_ip and
    BIO_accept.
  * Fixed the openssl(1) ca command so that is generates
    certificates with RFC 5280-conformant time.
  * Added ASN1_TIME_set_tm to set an asn1 from a struct tm *.
  * Added SSL{,_CTX}_set_{min,max}_proto_version() functions.
  * Added HKDF (HMAC Key Derivation Function) from BoringSSL
  * Providea a tls_unload_file() function that frees the memory
    returned from a tls_load_file() call, ensuring that it the
    contents become inaccessible. This is specifically needed on
    platforms where the library allocators may be different from
    the application allocator.
  * Perform reference counting for tls_config. This allows
    tls_config_free() to be called as soon as it has been passed
    to the final tls_configure() call, simplifying lifetime
    tracking for the application.
  * Moved internal state of SSL and other structures to be
    opaque.
  * Dropped cipher suites with DSS authentication.
* Thu Aug 24 2017 jengelh@inai.de
- Update to new upstream release 2.5.5
  * Distinguish between self-issued certificates and self-signed
    certificates. The certificate verification code has special
    cases for self-signed certificates and without this change,
    self-issued certificates (which it seems are common place
    with openvpn/easyrsa) were also being included in this
    category.
* Tue May  9 2017 tchvatal@suse.com
- Add conflict between libressl and the main versioned packages too
* Fri May  5 2017 tchvatal@suse.com
- Add conflict for split openssl packages
* Thu May  4 2017 jengelh@inai.de
- Update to new upstream release 2.5.4
  * Reverted a previous change that forced consistency between
    return value and error code when specifing a certificate
    verification callback, since this breaks the documented API.
  * Switched Linux getrandom() usage to non-blocking mode,
    continuing to use fallback mechanims if unsuccessful.
  * Fixed a bug caused by the return value being set early to
    signal successful DTLS cookie validation.
* Wed Apr 12 2017 jengelh@inai.de
- Update to new upstream release 2.5.1
  * Avoid a side-channel cache-timing attack that can leak the ECDSA
    private keys when signing. [bnc#1019334]
  * Detect zero-length encrypted session data early
  * Curve25519 Key Exchange support.
  * Support for alternate chains for certificate verification.
- Update to new upstream release 2.5.2
  * Added EVP interface for MD5+SHA1 hashes
  * Fixed DTLS client failures when the server sends a certificate
    request.
  * Corrected handling of padding when upgrading an SSLv2 challenge
    into an SSLv3/TLS connection.
  * Allowed protocols and ciphers to be set on a TLS config object
    in libtls.
- Update to new upstream release 2.5.3
  * Documentation updates
- Remove ecs.diff (merged)
* Mon Jan 23 2017 jengelh@inai.de
- Add ecs.diff [bnc#1019334]
* Thu Sep 29 2016 jengelh@inai.de
- Update to new upstream release 2.5.0
  * libtls now supports ALPN and SNI
  * libtls adds a new callback interface for integrating custom IO
  functions.
  * libtls now handles 4 cipher suite groups: "secure"
  (TLSv1.2+AEAD+PFS), "compat" (HIGH:!aNULL), "legacy"
  (HIGH:MEDIUM:!aNULL), "insecure" (ALL:!aNULL:!eNULL). This
  allows for flexibility and finer grained control, rather than
  having two extremes.
  * libtls now always loads CA, key and certificate files at the
  time the configuration function is called.
  * Add support for OCSP intermediate certificates.
  * Added functions used by stunnel and exim from BoringSSL - this
  brings in X509_check_host, X509_check_email, X509_check_ip, and
  X509_check_ip_asc.
  * Improved behavior of arc4random on Windows when using memory
  leak analysis software.
  * Correctly handle an EOF that occurs prior to the TLS handshake
  completing.
  * Limit the support of the "backward compatible" ssl2 handshake
  to only be used if TLS 1.0 is enabled.
  * Fix incorrect results in certain cases on 64-bit systems when
  BN_mod_word() can return incorrect results. BN_mod_word() now
  can return an error condition.
  * Added constant-time updates to address CVE-2016-0702
  * Fixed undefined behavior in BN_GF2m_mod_arr()
  * Removed unused Cryptographic Message Support (CMS)
  * More conversions of long long idioms to time_t
  * Reverted change that cleans up the EVP cipher context in
  EVP_EncryptFinal() and EVP_DecryptFinal(). Some software relies
  on the previous behaviour.
  * Avoid unbounded memory growth in libssl, which can be triggered
  by a TLS client repeatedly renegotiating and sending OCSP
  Status Request TLS extensions.
  * Avoid falling back to a weak digest for (EC)DH when using SNI
  with libssl.
* Wed Aug  3 2016 jengelh@inai.de
- Update to new upstream release 2.4.2
  * Ensured OSCP only uses and compares GENERALIZEDTIME values as
  per RFC6960. Also added fixes for OCSP to work with
  intermediate certificates provided in responses.
  * Fixed incorrect results from BN_mod_word() when the modulus is
  too large.
  * Correctly handle an EOF prior to completing the TLS handshake
  in libtls.
  * Removed flags for disabling constant-time operations. This
  removes support for DSA_FLAG_NO_EXP_CONSTTIME,
  DH_FLAG_NO_EXP_CONSTTIME, and RSA_FLAG_NO_CONSTTIME flags,
  making all of these operations unconditionally constant-time.
* Wed Aug  3 2016 jengelh@inai.de
- Update to new upstream release 2.4.2
  * Ensured OSCP only uses and compares GENERALIZEDTIME values as
  per RFC6960. Also added fixes for OCSP to work with
  intermediate certificates provided in responses.
  * Fixed incorrect results from BN_mod_word() when the modulus is
  too large.
  * Correctly handle an EOF prior to completing the TLS handshake
  in libtls.
* Fri Jun 10 2016 jengelh@inai.de
- Update to new upstream release 2.4.1
  * Correct a problem that prevents the DSA signing algorithm from
  running in constant time even if the flag BN_FLG_CONSTTIME is
  set.
* Thu Jun  2 2016 jengelh@inai.de
- Update to new upstream release 2.4.0
  * Added missing error handling around bn_wexpand() calls.
  * Added explicit_bzero calls for freed ASN.1 objects.
  * Fixed X509_*set_object functions to return 0 on allocation
  failure.
  * Implemented the IETF ChaCha20-Poly1305 cipher suites.
  * Changed default EVP_aead_chacha20_poly1305() implementation to
  the IETF version, which is now the default.
  * Fixed password prompts from openssl(1) to properly handle ^C.
  * Reworked error handling in libtls so that configuration errors
  are visible.
  * Deprecated internal use of EVP_[Cipher|Encrypt|Decrypt]_Final.
* Wed May  4 2016 jengelh@inai.de
- Update to new upstream release 2.3.4 [boo#978492, boo#977584]
  * Fix multiple vulnerabilities in libcrypto relating to ASN.1 and
  encoding.
* Wed Mar 23 2016 jengelh@inai.de
- Update to new upstream release 2.3.3
  * cert.pem has been reorganized and synced with Mozilla's
  certificate store
* Tue Feb  2 2016 jengelh@inai.de
- Update to new upstream release 2.3.2
  * Added EVP_aead_chacha20_poly1305_ietf() which matches the AEAD
  construction introduced in RFC 7539, which is different than
  that already used in TLS with EVP_aead_chacha20_poly1305().
  * Avoid a potential undefined C99+ behavior due to shift overflow
  in AES_decrypt.
- Remove 0001-Fix-for-OpenSSL-CVE-2015-3194.patch,
  0001-Fix-for-OpenSSL-CVE-2015-3195.patch (included)
* Fri Dec 11 2015 jengelh@inai.de
- Add 0001-Fix-for-OpenSSL-CVE-2015-3194.patch,
  0001-Fix-for-OpenSSL-CVE-2015-3195.patch [boo#958768]
* Wed Nov  4 2015 jengelh@inai.de
- Update to new upstream release 2.3.1
  * ASN.1 cleanups and RFC5280 compliance fixes.
  * Time representations switched from "unsigned long" to "time_t".
  LibreSSL now checks if the host OS supports 64-bit time_t.
  * Changed tls_connect_servername to use the first address that
  resolves with getaddrinfo().
  * Fixed a memory leak and out-of-bounds access in OBJ_obj2txt,
  * Fixed an up-to 7 byte overflow in RC4 when len is not a multiple
  of sizeof(RC4_CHUNK).
- Drop CVE-2015-5333_CVE-2015-5334.patch (merged)
* Fri Oct 16 2015 astieger@suse.com
- Security update for libressl:
  * CVE-2015-5333: Memory Leak [boo#950707]
  * CVE-2015-5334: Buffer Overflow [boo#950708]
- adding CVE-2015-5333_CVE-2015-5334.patch
* Thu Sep 24 2015 jengelh@inai.de
- Update to new upstream release 2.3.0
  * SSLv3 is now permanently removed from the tree.
  * libtls API: The read/write functions work correctly with external
  event libraries. See the tls_init man page for examples of using
  libtls correctly in asynchronous mode.
  * When using tls_connect_fds, tls_connect_socket or tls_accept_fds,
  libtls no longer implicitly closes the passed in sockets. The
  caller is responsible for closing them in this case.
  * Removed support for DTLS_BAD_VER. Pre-DTLSv1 implementations are
  no longer supported.
  * SHA-0 is removed, which was withdrawn shortly after publication
  20 years ago.
* Sun Aug 30 2015 jengelh@inai.de
- Update to new upstream release 2.2.3
  * LibreSSL 2.2.2 incorrectly handles ClientHello messages that do
  not include TLS extensions, resulting in such handshakes being
  aborted. This release corrects the handling of such messages.
* Mon Aug 17 2015 jengelh@inai.de
- drop /etc/ssl/cert.pem
* Mon Aug 17 2015 jengelh@inai.de
- Avoid file conflict with ca-certificates by dropping
  /etc/ssl/certs
* Sun Aug  9 2015 jengelh@inai.de
- Update to new upstream release 2.2.2
  * Incorporated fix for OpenSSL issue #3683
  [malformed private key via command line segfaults openssl]
  * Removed workarounds for TLS client padding bugs, removed
  SSLv3 support from openssl(1), removed IE 6 SSLv3 workarounds,
  removed RSAX engine.
  * Modified tls_write in libtls to allow partial writes, clarified with
  examples in the documentation.
  * Building a program that intentionally uses SSLv3 will result in
  a linker warning.
  * Added TLS_method, TLS_client_method and TLS_server_method as a
  replacement for the SSLv23_*method calls.
  * Switched `openssl dhparam` default from 512 to 2048 bits
  * Fixed `openssl pkeyutl -verify` to exit with a 0 on success
  * Fixed dozens of Coverity issues including dead code, memory leaks,
  logic errors and more.
* Mon Jul 13 2015 astieger@suse.com
- Update to new upstream release 2.2.1 [bnc#937891]
  * Protocol parsing conversions to BoringSSL's CRYPTO ByteString
  (CBS) API
  * Added EC_curve_nid2nist and EC_curve_nist2nid from OpenSSL
  * Removed Dynamic Engine support
  * Removed unused and obsolete MDC-2DES cipher
  * Removed workarounds for obsolete SSL implementations
  * Fixes and changes for plaforms other than GNU/Linux
* Fri Jun 12 2015 jengelh@inai.de
- Update to new upstream release 2.2.0
  * Removal of OPENSSL_issetugid and all library getenv calls.
  Applications can and should no longer rely on environment
  variables for changing library behavior.
  OPENSSL_CONF/SSLEAY_CONF is still supported with the openssl(1)
  command.
  * libtls API and documentation additions
  * fixed:
  * CVE-2015-1788: Malformed ECParameters causes infinite loop
  * CVE-2015-1789: Exploitable out-of-bounds read in X509_cmp_time
  * CVE-2015-1792: CMS verify infinite loop with unknown hash
  function (this code is not enabled by default)
  * already fixed earlier, or not found in LibreSSL:
  * CVE-2015-4000: DHE man-in-the-middle protection (Logjam)
  * CVE-2015-1790: PKCS7 crash with missing EnvelopedContent
  * CVE-2014-8176: Invalid free in DTLS
* Wed Mar 25 2015 jengelh@inai.de
- Ship pkgconfig files again
* Thu Mar 19 2015 jengelh@inai.de
- Update to new upstream release 2.1.6
  * Reject server ephemeral DH keys smaller than 1024 bits
  * Fixed CVE-2015-0286 - Segmentation fault in ASN1_TYPE_cmp
  * Fixed CVE-2015-0287 - ASN.1 structure reuse memory corruption
  * Fixed CVE-2015-0289 - PKCS7 NULL pointer dereferences
  * Fixed CVE-2015-0209 - Use After Free following d2i_ECPrivatekey error
  * Fixed CVE-2015-0288 - X509_to_X509_REQ NULL pointer deref
* Fri Mar  6 2015 sor.alexei@meowr.ru
- Update to 2.1.4:
  * Improvements to libtls:
  - a new API for loading CA chains directly from memory instead
    of a file, allowing verification with privilege separation in
    a chroot without direct access to CA certificate files.
  - Ciphers default to TLSv1.2 with AEAD and PFS.
  - Improved error handling and message generation.
  - New APIs and improved documentation.
  * Add X509_STORE_load_mem API for loading certificates from memory.
    This facilitates accessing certificates from a chrooted
    environment.
  * New AEAD "MAC alias" allows configuring TLSv1.2 AEAD ciphers by
    using 'TLSv1.2+AEAD' as the cipher selection string.
  * New openssl(1) command 'certhash' replaces the c_rehash script.
  * Server-side support for TLS_FALLBACK_SCSV for compatibility
    with various auditor and vulnerability scanners.
  * Dead and disabled code removal including MD5, Netscape
    workarounds, non-POSIX IO, SCTP, RFC 3779 support,
    "#if 0" sections, and more.
  * The ASN1 macros are expanded to aid readability and
    maintainability.
  * Various NULL pointer asserts removed in favor of letting the
    OS/signal handler catch them.
  * Refactored argument handling in openssl(1) for consistency and
    maintainability.
  * Support for building with OPENSSL_NO_DEPRECATED.
  * Dozens of issues found with the Coverity scanner fixed.
  * Fix a minor information leak that was introduced in t1_lib.c
    r1.71, whereby an additional 28 bytes of .rodata (or .data) is
    provided to the network. In most cases this is a non-issue
    since the memory content is already public.
  * Fixes for the following low-severity issues were integrated
    into LibreSSL from OpenSSL 1.0.1k:
  - CVE-2015-0205 - DH client certificates accepted without
    verification.
  - CVE-2014-3570 - Bignum squaring may produce incorrect results.
  - CVE-2014-8275 - Certificate fingerprints can be modified.
  - CVE-2014-3572 - ECDHE silently downgrades to ECDH [Client].
* Wed Jan 28 2015 jengelh@inai.de
- Add package signatures
* Sat Jan 24 2015 jengelh@inai.de
- Update to new upstream release 2.1.3
  * Fixes for various memory leaks in DTLS, including those for
  CVE-2015-0206.
  * Application-Layer Protocol Negotiation (ALPN) support.
  * Simplfied and refactored SSL/DTLS handshake code.
  * SHA256 Camellia cipher suites for TLS 1.2 from RFC 5932.
  * Ensure the stack is marked non-executable for assembly sections.
* Fri Dec 12 2014 jengelh@inai.de
- Update to new upstream release 2.1.2
  * The two cipher suites GOST and Camellia have been reworked or
  reenabled, providing better interoperability with systems around
  the world.
  * The libtls library, a modern and simplified interface for secure
  client and server communications, is now packaged.
  * Assembly acceleration of various algorithms (most importantly
  AES, MD5, SHA1, SHA256, SHA512) are enabled for AMD64.
- Remove libressl-no-punning.diff (file to patch is gone)
* Wed Dec  3 2014 jengelh@inai.de
- Update to new upstream release 2.1.1
  * Address POODLE attack by disabling SSLv3 by default
  * Fix Eliptical Curve cipher selection bug
* Sat Aug  9 2014 jengelh@inai.de
- Update to new upstream release 2.0.5
  * This version forward-ports security fixes from OpenSSL 1.0.1i:
  CVE-2014-3506, CVE-2014-3507, CVE-2014-3508 (partially
  vulnerable), CVE-2014-3509, CVE-2014-3510, CVE-2014-3511.
  (LibreSSL was found not to be vulnerable to
  CVE-2014-3502, CVE-2014-3512, CVE-2014-5139)
* Wed Aug  6 2014 jengelh@inai.de
- Update to new upstream release 2.0.4
  * This version includes more portability changes, as well as other
  work. most noticable may be the deletion of the of the SRP code
  (which has not been enabled in any LibreSSL release).
- Remove pkg-config files so "pkgconfig(libcrypto)" remains
  unambiguous in the distro
* Tue Jul 22 2014 jengelh@inai.de
- Update to new upstream release 2.0.3
  * This release includes a number of portability fixes, and also
  includes some improvements to the fork detection support.
- Remove libressl-auxdal.diff, libressl-asn1test.diff
  (solved upstream)
* Wed Jul 16 2014 jengelh@inai.de
- Update to new upstream release 2.0.2
  * This release addresses the Linux forking and pid wrap issue
  reported recently.
- Add libressl-auxval.diff (fix compile error),
  libressl-asn1test.diff (fix testsuite failure)
* Sun Jul 13 2014 jengelh@inai.de
- Update to new upstream release 2.0.1
  * This release includes a number of portability fixes based on
  the initial feedback received. A few hardcoded compiler options
  that were problematic on some systems as well as -Werror have
  been removed. This release also includes pkg-config support.
- Remove libressl-rt.diff (solved differently upstream)
* Sat Jul 12 2014 jengelh@inai.de
- Initial package (version 2.0.0) for build.opensuse.org
- Add libressl-no-punning.diff, libressl-rt.diff to fix build
  errors
