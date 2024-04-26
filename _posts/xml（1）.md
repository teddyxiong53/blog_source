---
title: xml（1）
date: 2024-04-25 10:39:17
tags:
	- xml

---

--

本来我对xml是没有太多好感的。

但是我现在打算给lvlg做一个布局描述系统。

想了想，好像在布局描述这一块，没有比xml更好的。

android都是大量使用xml来布局。

那就研究一下。

# xml简介

XML（可扩展标记语言）是一种用于描述和存储数据的标记语言。

它是一种通用的标记语言，设计用来传输和存储数据，旨在促进信息共享和数据交换。

XML通过使用自定义的标记来组织数据，使得数据可以按照层次结构进行组织和表示。

以下是XML的一些关键特点和用途：

1. **可扩展性（Extensibility）**：XML允许用户定义自己的标记，因此非常灵活，可以用于各种不同的应用场景。

2. **层次性（Hierarchy）**：XML数据被组织成树形结构，具有层次性，可以表示复杂的数据关系。

3. **自描述性（Self-Descriptiveness）**：XML文档包含了自己的元数据（标签），因此具有自描述性，能够清晰地表达数据的含义和结构。

4. **跨平台性（Platform Independence）**：XML是一种与平台无关的标记语言，可以在各种不同的计算机系统和软件应用中使用。

5. **广泛应用**：XML在各种领域都有广泛的应用，包括Web开发、数据交换、配置文件、文档标记等。

6. **与HTML的关系**：XML与HTML有密切的关系，但XML更加通用和灵活，不受HTML的严格规则限制。

XML通常以文本形式存储，使用角括号和标签来定义数据的结构和内容。例如：

```xml
<bookstore>
  <book category="Fiction">
    <title>Harry Potter</title>
    <author>J.K. Rowling</author>
    <year>2005</year>
    <price>29.99</price>
  </book>
  <book category="Non-Fiction">
    <title>Learning XML</title>
    <author>Erik T. Ray</author>
    <year>2003</year>
    <price>39.95</price>
  </book>
</bookstore>
```

在这个例子中，`<bookstore>` 是根元素，它包含两个 `<book>` 元素，每个 `<book>` 元素又包含了 `title`, `author`, `year`, 和 `price` 等子元素，以及 `category` 属性。

XML的灵活性和自描述性使其成为数据交换和存储的一种重要格式，在Web服务、配置文件、数据库导出等方面都得到了广泛的应用。

# xml发展历史

XML的发展历史可以追溯到上世纪90年代初，以下是XML的主要发展阶段和里程碑：

1. **起源（1996年）**：XML的起源可以追溯到1996年，当时，一些计算机公司（包括微软、Sun Microsystems、IBM等）合作制定了XML 1.0规范，以取代SGML（标准通用标记语言）。

2. **XML 1.0（1998年）**：1998年2月10日，W3C（万维网联盟）发布了XML 1.0规范，这是XML的首个正式版本。XML 1.0规范确立了XML的基本语法、元素和属性的定义，以及文档的结构和解析规则。

3. **XML的广泛应用（1998年至今）**：随着XML的发布，它迅速成为互联网和软件开发领域的重要标准。XML被广泛应用于Web服务、数据交换、配置文件、文档标记等方面。许多软件和技术（如SOAP、RSS、Atom等）都采用XML作为数据交换的基础格式。

4. **XML家族的扩展（2000年至今）**：在XML的基础上，衍生出了许多相关技术和标准，构成了XML家族，包括XPath、XSLT、XML Schema、XQuery等，这些技术为XML的处理、转换和验证提供了丰富的支持。

5. **XML 1.1（2004年）**：==2004年8月，W3C发布了XML 1.1规范，这是对XML 1.0的扩展和修订版本。==XML 1.1引入了一些新的特性和语法规则，同时修正了一些XML 1.0中的问题，但由于兼容性和实现成本等原因，==XML 1.1并没有得到广泛采用，许多应用仍然沿用XML 1.0。==

6. **XML的持续发展（2000年至今）**：自2000年以来，XML一直在持续发展和演进。W3C和其他组织不断推出新的XML技术和规范，以满足不断变化的需求和挑战，例如，XML的序列化和解析性能优化、语义标记（如RDF、OWL等）、语义Web等领域的研究和标准化工作。

总的来说，XML作为一种通用的数据标记语言，已经成为互联网和软件开发领域的重要基础技术之一，在数据交换、存储、处理和展示方面发挥着重要作用。

# xml1.0和xml1.1的区别

XML 1.0和XML 1.1是XML标准的两个主要版本，在语法和特性上有一些区别，以下是它们之间的主要区别：

1. **字符集限制**：
   - XML 1.0仅支持Unicode字符范围内的字符，包括Unicode字符范围内的所有字符，但不包括Unicode保留字符。
   - XML 1.1允许使用Unicode字符范围内的所有字符，包括一些XML 1.0中被保留的Unicode字符，例如“八进制数值实体引用”，这些字符在XML 1.0中是无效的。

2. **命名限制**：
   - XML 1.0的命名规则要求名称中的第一个字符必须是字母（包括扩展的Unicode字母）或者下划线“_”，后续字符可以是字母、数字、连字符“-”或者下划线“_”。
   - XML 1.1的命名规则更加宽松，允许名称中的第一个字符可以是任何Unicode字符，包括标点符号和数字等。

3. **换行符处理**：
   - XML 1.0中规定换行符只能使用LF（Line Feed，"\n"）或CR（Carriage Return，"\r"）字符。
   - XML 1.1允许使用LF、CR、或CRLF（Carriage Return + Line Feed，"\r\n"）作为换行符。

4. **XML声明**：
   - XML 1.0中XML声明的版本号必须是1.0。
   - XML 1.1中XML声明的版本号可以是1.0或1.1。

5. **规范性**：
   - XML 1.0是W3C的推荐标准。
   - XML 1.1也是W3C的推荐标准，但由于一些兼容性问题和实现复杂性，许多应用仍然沿用XML 1.0。

总的来说，XML 1.1相对于XML 1.0来说在字符集、命名规则和换行符处理等方面更加宽松，但由于兼容性和实现复杂性的考虑，许多应用仍然选择使用XML 1.0。选择使用哪个版本取决于具体应用的需求和兼容性要求。

# 一个典型的xml文件，可以体现出xml的所有特性

以下是一个典型的XML文件，展示了XML的各种特性：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE bookstore [
  <!ELEMENT bookstore (book+)>
  <!ELEMENT book (title, author, year, price)>
  <!ATTLIST book category CDATA #REQUIRED>
]>
<bookstore>
  <book category="Fiction">
    <title>Harry Potter</title>
    <author>J.K. Rowling</author>
    <year>2005</year>
    <price>29.99</price>
  </book>
  <book category="Non-Fiction">
    <title>Learning XML</title>
    <author>Erik T. Ray</author>
    <year>2003</year>
    <price>39.95</price>
  </book>
</bookstore>
```

这个XML文件展示了以下特性：

1. **XML声明**：`<?xml version="1.0" encoding="UTF-8"?>`，指定了XML版本和字符编码。
  
2. **DTD（文档类型定义）**：通过`<!DOCTYPE>`声明书店文档的结构和规则，定义了元素和属性的结构。

3. **根元素**：`<bookstore>`，作为XML文档的根元素，包含了所有其他元素。

4. **元素**：`<book>`，表示书籍信息；`<title>`、`<author>`、`<year>`、`<price>`表示书籍的标题、作者、出版年份和价格。

5. **属性**：`category`，定义在`<book>`元素上，用于描述书籍的类别。

6. **元素内容**：`<title>`、`<author>`、`<year>`、`<price>`元素内包含了文本内容，分别表示书籍的标题、作者、出版年份和价格。

7. **DTD中的元素和属性规范**：`<!ELEMENT>`用于定义元素的内容，`<!ATTLIST>`用于定义属性。

8. **CDATA类型**：在`<!ATTLIST>`中，`CDATA`表示属性值是字符数据，不需要进行转义。

这个XML文件包含了XML的基本语法、元素、属性、DTD的使用等多个特性，展示了XML作为一种通用的数据标记语言的强大灵活性。

## DTD 可以没有吗？

是的，可以创建没有DTD的XML文件。DTD（文档类型定义）是一种可选的机制，用于定义XML文档的结构和规则，但并不是XML文件必须具备的要素。许多XML文件在实际应用中并不使用DTD，而是依赖其他机制来验证和解析文件，比如XML Schema、RELAX NG、或者直接通过程序代码进行验证。

如果XML文件不包含DTD，则其结构和内容仅由XML本身的语法规则来约束，而不受DTD的影响。这种情况下，XML文件的结构和规则完全由文件作者自行定义，但也可能导致文件在解析和处理时缺乏统一的约束和规范，可能会增加数据解析的复杂性和不确定性。

在实际应用中，是否使用DTD取决于具体的需求和情况。一些简单的XML文件可能不需要DTD，而一些复杂的XML文件可能需要使用XML Schema或其他验证机制来确保数据的有效性和一致性。

# buildroot里的xml package有哪些

ezxml 
ezXML 是一个 C 库，用于解析受 PHP 的 simpleXML 启发的 XML 文档。顾名思义，它易于使用。它非常适合解析 XML 配置文件或 REST Web 服务响应。它也快速且轻量级（编译不到 20k）。
https://ezxml.sourceforge.net/

libroxml
该库是用于 XML 文件解析的最小、易于使用的 C 实现，
剥离的二进制文件约为 50K。公共 API 定义了不到 30 个函数来完成您需要的所有操作，因此非常容易上手。
https://github.com/blunderer/libroxml.git 
因为 XML 解析总是很难重新发明，而且 XML 库通常太大而无法容纳很少的应用程序。Libroxml 主要针对嵌入式软件和环境，但您可以在需要处理 XML 时使用它，因为 libroxml 轻巧且快速。

libxml2
这个是gnome项目的一部分。
那么就是功能强大，但是相对比较复杂的实现了。

libxmlpp
这个是c++包装的libxml

rapidxml
RapidXml 试图创建最快的 XML 解析器，同时保留可用性、可移植性和合理的 W3C 兼容性。它是用现代 C++ 编写的原位解析器，解析速度接近对相同数据执行的 strlen 函数的解析速度。

tinyxml
TinyXML-2 长期以来一直是所有开发的重点。它已经过很好的测试，应该用来代替 TinyXML-1。
TinyXML-2 是一个简单、小巧、高效的 C++ XML 解析器，可以很容易地集成到其他程序中。

## 性能测试对比

8MB的xml文件，一行30个属性，有1W多行

注：以下数据仅作参考，与机器等环境有关。
tinyxml：1830ms
rapidxml：130ms
pugixml：110ms


从接口上来讲，tinyxml、pugixml很近似
从名气来讲，rapidxml貌似是boost选用的，应该更出名吧。

由于之前一直使用tinyxml，选用pugixml。

https://www.cnblogs.com/lcinx/p/10570836.html