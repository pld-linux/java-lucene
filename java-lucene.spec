
# Conditional build:
%bcond_with		javadoc		# build Lucene javadoc
%bcond_with		contrib		# build Lucene contributed extensions

%define		contrib_ver	2.4
%define 	srcname	lucene
%include	/usr/lib/rpm/macros.java
Summary:	Text search engine library in Java
Name:		java-%{srcname}
Version:	3.6.2
Release:	0.1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/lucene/java/%{version}/lucene-%{version}-src.tgz
# Source0-md5:	e438b947ab71866ee77a55248d6ec985
Source1:	je-4.1.6.jar
# Source1-md5:	b7cd75e409267b903c3cb8e1da1856e9
Patch0:		%{name}-test.patch
Patch1:		%{name}-je_jar.patch
URL:		http://lucene.apache.org/
BuildRequires:	ant
BuildRequires:	db-java
BuildRequires:	java-commons-digester
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
%if %{with contrib}
BuildRequires:  icu4j
%endif
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache Lucene is a high-performance, full-featured text search engine
library written entirely in Java. It is a technology suitable for
nearly any application that requires full-text search, especially
cross-platform.

%package contrib
Summary:	Contrib packages for lucene
Group:		Libraries/Java
Requires:	%{name} = %{version}

%description contrib
Contrib packages for lucene.

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
#%patch0 -p1
#%patch1 -p1

# FIXME: move je.jar to separate spec and use it via CLASSPATH
install -d contrib/db/bdb-je/lib
cp -p %{SOURCE1} contrib/db/bdb-je/lib/je.jar

%build
CLASSPATH=$(build-classpath commons-digester db)

export LC_ALL=en_US

install -d build
%ant \
	-Dversion=%{version} \
	-Dbuild.sysclasspath=only

%if %{with contrib}
cd contrib
CONTRIB_PACKAGES="analyzers benchmark db highlighter instantiated lucli memory miscellaneous queries regex similarity snowball spellchecker surround swing wikipedia wordnet xml-query-parser"
for i in $CONTRIB_PACKAGES; do
	cd $i
	install -d build
	%ant
	cd -
done
cd ..
%endif

%if %{with javadoc}
%javadoc -d apidocs \
	org.apache.lucene \
	$(find src/java/org/apache/lucene -name '*.java')
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

cp -a build/core/%{srcname}-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-core-%{version}.jar
ln -s %{srcname}-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-core.jar
ln -s %{srcname}-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

%if %{with contrib}
CONTRIB_PACKAGES="analyzers benchmark highlighter instantiated lucli memory misc queries regex similarity snowball spellchecker surround swing wikipedia wordnet xml-query-parser"
for i in $CONTRIB_PACKAGES; do
	cp -a build/contrib/$i/%{srcname}-$i-%{contrib_ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-$i-%{contrib_ver}.jar
	ln -s %{srcname}-$i-%{contrib_ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-$i.jar
	%jar -cf %{srcname}-$i-%{contrib_ver}.jar -C build/contrib/$i/classes/java .
done
cp -p build/contrib/db/bdb/%{srcname}-bdb-%{contrib_ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-bdb-%{contrib_ver}.jar
ln -s %{srcname}-bdb-%{contrib_ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-bdb.jar
cp -p build/contrib/db/bdb-je/%{srcname}-bdb-je-%{contrib_ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-bdb-je-%{contrib_ver}.jar
ln -s %{srcname}-bdb-je-%{contrib_ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-bdb-je.jar
%endif

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
%{_javadir}/%{srcname}-core-%{version}.jar
%{_javadir}/%{srcname}-core.jar
%{_javadir}/%{srcname}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif

%if %{with contrib}
%files contrib
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-analyzers-%{contrib_ver}.jar
%{_javadir}/%{srcname}-analyzers.jar
%{_javadir}/%{srcname}-bdb-%{contrib_ver}.jar
%{_javadir}/%{srcname}-bdb-je-%{contrib_ver}.jar
%{_javadir}/%{srcname}-bdb-je.jar
%{_javadir}/%{srcname}-bdb.jar
%{_javadir}/%{srcname}-benchmark-%{contrib_ver}.jar
%{_javadir}/%{srcname}-benchmark.jar
%{_javadir}/%{srcname}-highlighter-%{contrib_ver}.jar
%{_javadir}/%{srcname}-highlighter.jar
%{_javadir}/%{srcname}-instantiated-%{contrib_ver}.jar
%{_javadir}/%{srcname}-instantiated.jar
%{_javadir}/%{srcname}-lucli-%{contrib_ver}.jar
%{_javadir}/%{srcname}-lucli.jar
%{_javadir}/%{srcname}-memory-%{contrib_ver}.jar
%{_javadir}/%{srcname}-memory.jar
%{_javadir}/%{srcname}-misc-%{contrib_ver}.jar
%{_javadir}/%{srcname}-misc.jar
%{_javadir}/%{srcname}-queries-%{contrib_ver}.jar
%{_javadir}/%{srcname}-queries.jar
%{_javadir}/%{srcname}-regex-%{contrib_ver}.jar
%{_javadir}/%{srcname}-regex.jar
%{_javadir}/%{srcname}-similarity-%{contrib_ver}.jar
%{_javadir}/%{srcname}-similarity.jar
%{_javadir}/%{srcname}-snowball-%{contrib_ver}.jar
%{_javadir}/%{srcname}-snowball.jar
%{_javadir}/%{srcname}-spellchecker-%{contrib_ver}.jar
%{_javadir}/%{srcname}-spellchecker.jar
%{_javadir}/%{srcname}-surround-%{contrib_ver}.jar
%{_javadir}/%{srcname}-surround.jar
%{_javadir}/%{srcname}-swing-%{contrib_ver}.jar
%{_javadir}/%{srcname}-swing.jar
%{_javadir}/%{srcname}-wikipedia-%{contrib_ver}.jar
%{_javadir}/%{srcname}-wikipedia.jar
%{_javadir}/%{srcname}-wordnet-%{contrib_ver}.jar
%{_javadir}/%{srcname}-wordnet.jar
%{_javadir}/%{srcname}-xml-query-parser-%{contrib_ver}.jar
%{_javadir}/%{srcname}-xml-query-parser.jar
%endif
