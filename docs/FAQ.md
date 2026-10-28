# Perguntas Frequentes

**Preciso usar uma ferramenta, linguagem ou formato específico?**
Não. Escolha o que você domina e consiga justificar. Python e Java são as linguagens mais usadas pela equipe, mas qualquer stack é aceita.

**Preciso usar Spark/Hadoop/Cloudera?**
Não. O volume cabe em uma máquina comum. Se escolher Spark, ótimo, mas justifique. Escolher a ferramenta certa para o tamanho do problema também é um critério.

**Posso usar bibliotecas de qualidade de dados (Great Expectations, Pandera, Soda...)?**
Pode, desde que você entenda e consiga explicar as regras que configurou.

**O arquivo CSV está estranho (acentos quebrados, vírgula no decimal). É erro?**
Não. Codificação ISO-8859-1, separador `;` e vírgula decimal são intencionais. Lidar com isso faz parte da ingestão.

**Posso corrigir tudo à mão no CSV?**
Não. Tudo deve ser feito por código reproduzível.

**Quantas linhas "sujas" existem? Qual a lista de problemas?**
Não informamos. Explore os dados, compare com o dicionário e descubra.

**Devo descartar uma linha com problema ou corrigi-la?**
Depende. Corrija quando o valor correto puder ser **deduzido com segurança**; anule o campo ou rejeite a linha quando não puder. O importante é decidir com critério e **documentar** em `docs/DECISOES_QUALIDADE.md`.

**Posso usar dados externos no enriquecimento?**
Sim, desde que sejam **públicos e de licença aberta**, e que você **cite fonte e licença**. Se o pipeline depender de internet, explique o que acontece sem ela (por exemplo, guardar uma cópia local versionada do dado externo).

**Posso usar ferramentas de IA (ChatGPT, Claude, Copilot...)?**
Sim, são ferramentas do dia a dia de qualquer profissional de dados. Pedimos três coisas:
1. **Declare** no README quais ferramentas usou e para quê.
2. **Domine o que entregou.** Na apresentação você explicará seu código e suas decisões, e lançaremos perguntas de aprofundamento.
3. **Valide.** Código gerado por IA precisa ser testado contra o dicionário. Quem apenas cola resultado sem verificar costuma entregar prata com erros.

**Posso conversar com outros candidatos ou pedir ajuda a terceiros?**
O trabalho deve ser **individual**. Consultar documentação, artigos e tutoriais é normal. Pedir a outra pessoa que faça o desafio por você não é.

**Meu painel precisa ser bonito?**
Precisa ser **claro e útil**. Um painel simples que responde bem às perguntas vale mais que um enfeitado.

**Não consegui terminar tudo. O que faço?**
Entregue o que funciona de ponta a ponta e documente o que faltou e como você continuaria. Preferimos uma entrega pequena e sólida a uma grande e quebrada.

**O container precisa funcionar em Windows, Linux e Mac?**
Seu passo a passo deve informar em qual sistema você testou. Evite caminhos fixos de uma máquina específica e use volumes do Docker.

**Tive um problema técnico com o kit (arquivo corrompido, dúvida no dicionário).**
Escreva para a equipe de seleção. Respondemos para todos os candidatos o que for esclarecimento geral, para manter a igualdade de condições.
