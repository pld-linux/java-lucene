
# Conditional build:
%bcond_with		javadoc		# build Lucene javadoc
%bcond_without		contrib		# build Lucene contributed extensions

%define 	srcname	lucene
%include	/usr/lib/rpm/macros.java
Summary:	Text search engine library in Java
Name:		java-%{srcname}
Version:	3.6.2
Release:	0.1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://archive.apache.org/dist/lucene/java/%{version}/lucene-%{version}-src.tgz
# Source0-md5:	e438b947ab71866ee77a55248d6ec985
Source1:	je-4.1.6.jar
# Source1-md5:	b7cd75e409267b903c3cb8e1da1856e9
Patch0:		%{name}-test.patch
Patch1:		%{name}-je_jar.patch
URL:		http://lucene.apache.org/
BuildRequires:	ant
BuildRequires:	db-java
BuildRequires:	java-commons-compress
BuildRequires:	java-commons-digester
BuildRequires:	java-ivy
BuildRequires:	java-jtidy
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
%if %{with contrib}
BuildRequires:	java-icu4j
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
required_jars="jtidy regexp commons-digester commons-compress ivy"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

# source code not US-ASCII
export LC_ALL=en_US

install -d build
%ant \
	-Divy.settings.file=ivy-conf.xml \
	-Dbuild.sysclasspath=first \
	-Djavacc.home=%{_bindir}/javacc \
	-Djavacc.jar=%{_javadir}/javacc.jar \
	-Djavacc.jar.dir=%{_javadir} \
	-Djavadoc.link=file://%{_javadocdir}/java \
	-Dversion=%{version} \
	-Dfailonjavadocwarning=false \
	-Dmaven-tasks.uptodate=true \
	jar-lucene-core docs javadocs-core

%if %{with contrib}
required_jars="jtidy regexp commons-digester commons-compress icu4j ivy"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH
%ant \
	-Divy.settings.file=ivy-conf.xml \
	-Dbuild.sysclasspath=first \
	-Djavacc.home=%{_bindir}/javacc \
	-Djavacc.jar=%{_javadir}/javacc.jar \
	-Djavacc.jar.dir=%{_javadir} \
	-Djavadoc.link=file://%{_javadocdir}/java \
	-Dversion=%{version} \
	-Dfailonjavadocwarning=false \
	-Dmaven-tasks.uptodate=true \
	jar-test-framework javadocs build-contrib
%endif

%if %{with javadoc}
%javadoc -d apidocs \
	org.apache.lucene \
	$(find src/java/org/apache/lucene -name '*.java')
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

cp -p build/core/%{srcname}-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-core-%{version}.jar
ln -s %{srcname}-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-core.jar
ln -s %{srcname}-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

%if %{with contrib}
# contrib jars
install -d $RPM_BUILD_ROOT%{_javadir}/%{srcname}-contrib
for c in benchmark demo facet grouping highlighter icu instantiated join memory misc pruning queries queryparser remote spatial spellchecker xml-query-parser; do
	cp -p build/contrib/$c/%{srcname}-${c}-%{version}.jar \
		$RPM_BUILD_ROOT%{_javadir}/%{srcname}-contrib/%{srcname}-${c}.jar
done

# contrib analyzers
for c in analyzers kuromoji phonetic smartcn stempel; do
	cp -p build/contrib/analyzers/*/%{srcname}-${c}-%{version}.jar \
		$RPM_BUILD_ROOT%{_javadir}/%{srcname}-contrib/%{srcname}-${c}.jar
done
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
%dir %{_javadir}/lucene-contrib
%{_javadir}/%{srcname}-contrib/%{srcname}-analyzers.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-benchmark.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-demo.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-facet.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-grouping.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-highlighter.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-icu.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-instantiated.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-join.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-kuromoji.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-memory.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-misc.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-phonetic.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-pruning.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-queries.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-queryparser.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-remote.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-smartcn.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-spatial.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-spellchecker.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-stempel.jar
%{_javadir}/%{srcname}-contrib/%{srcname}-xml-query-parser.jar
%endif
