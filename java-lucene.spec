%bcond_without  javadoc         # don't build javadoc
%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif
#
%include	/usr/lib/rpm/macros.java
#
%define 	srcname	lucene

Summary:	Text search engine library in Java
Name:		java-%{srcname}
Version:	2.4.1
Release:	2
License:	Apache v2.0
Group:		Development/Languages/Java
Source0:	http://www.apache.net.pl/lucene/java/lucene-%{version}-src.tar.gz
# Source0-md5:	ad46595439240e10387fcbf7647705db
Patch0:		%{name}-test.patch
URL:		http://lucene.apache.org/
BuildRequires:	java-commons-digester
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache Lucene is a high-performance, full-featured text search engine
library written entirely in Java. It is a technology suitable for
nearly any application that requires full-text search, especially
cross-platform.

%package javadoc
Summary:	Online manual for lucene
Summary(pl.UTF-8):	Dokumentacja online do lucene
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for lucene.

%description javadoc -l pl.UTF-8
Dokumentacja do lucene.

%description javadoc -l fr.UTF-8
Javadoc pour lucene.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1

%build
CLASSPATH=$(build-classpath commons-digester)

install -d build
%ant -Dbuild.sysclasspath=only

%if %{with javadoc}
%javadoc -d apidocs \
	%{?with_java_sun:org.apache.lucene} \
	$(find src/java/org/apache/lucene -name '*.java')
%endif

%jar -cf %{srcname}-%{version}.jar -C build .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
