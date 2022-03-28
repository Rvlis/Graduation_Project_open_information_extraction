# 开放信息抽取

## 环境要求和配置✔
### 环境要求：
   python-3.6+, Java-1.8, maven-3.0.4
### 环境配置：
1. 克隆该仓库
   ```bash
   git clone https://github.com/Rvlis/Open_Information_Extraction.git
   cd Open_Information_Extraction
   ```

2. 安装包 `pip install -r requirements.txt`
   
3. 安装 __stanza__，stanza支持通过python接口访问JAVA编写的自然语言处理工具 __Stanford CoreNLP__
   ```bash
   git clone https://github.com/Rvlis/stanza.git
   cd stanza
   pip install -e .
   ```

4. 安装 __Stanford CoreNLP__
   ```bash
   cd Open_Information_Extraction
   python
   ```
   ```python
   import stanza
   stanza.install_corenlp("路径值，绝对路径，建议放在Open_Information_Extraction目录下")
   ```

5. 添加环境变量
   `CORENLP_HOME` = `4.中路径值`
    <div align="center">
      <img src="./img/添加环境变量.jpg" width = "80%" alt="添加环境变量" align=center />
    </div>

6. 安装 __neuralcoref__ 实现共指消解
   ```bash
   git clone https://github.com/Rvlis/neuralcoref.git
   cd neuralcoref
   pip install -r requirements.txt
   pip install -e .
   ```

7. 安装Spacy预训练模型，下载[该链接](https://github.com/explosion/spacy-models/releases/tag/en_core_web_md-2.3.1)下的 `.tar.gz`文件并安装
   ```bash
   cd Open_Information_Extraction
   pip install en_core_web_md-2.3.1.tar.gz
   ```

8. 环境配置完成后，运行demo，对单句进行关系三元组抽取
   ```python
   cd OIE/src
   python run.py
   ```
   得到以下输出结果
   ```python
   >>> Bell, a telecommunication company, which is based in Los Angeles --> (Bell; is based in; Los Angeles)
   >>> Bell, a telecommunication company, which is based in Los Angeles --> (Bell; "is" ; a telecommunication company)
   ```

## 复合句简化
### 要求：
阅读以下参考文献或任何其他参考资料，了解复合句简化阶段的原理，毕设答辩时能应对老师的提问即可
### 参考文献：
[Context-Preserving Text Simplification](./paper/Context-Preserving-Text-Simplification.pdf)
### 参考代码：
__[OIE/src/C2S_part/](./OIE/src/C2S_part/)__: C2S(Complex To Simple)，复合句简化，基于stanford corenlp工具实现，所以为java代码 

## 实体抽取
### 要求：
### 参考代码：
__[OIE/src/NER_part/corenlp_chunk_candidate_relations_triples.py](./OIE/src/NER_part/corenlp_chunk_candidate_relations_triples.py)__
1. 基于规则的显式短语识别
   这一步中显式短语的识别方法是通过 __建立关于词性标注（POS tagging，part-of-speech tagging）的正则表达式__ (19~59)
   <div align="center">
      <img src="./img/基于规则的显示短语识别.jpg" width = "80%" alt="添加环境变量" align=center />
   </div>
2. 基于深度学习的显式短语识别
3. 隐式短语扩展

## 关系抽取

## 生成关系三元组

## 性能评估