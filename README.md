# Trabalho 1 - Aprendizado de Máquina - INF01017 UFRGS

## Instruções de execução:

Para executar qualquer dataset além dos providos na pasta *dataset*, é necessário prover um arquivo de metadados seguindo o padrão de nome *nome_do_arq_sem_extensao*_metadata.csv. Também é necessário alterar o delimitador no arquivo main.py caso o delimitador dos dados do arquivo seja diferente de TAB.

A execução realiza os experimentos que incluem variação do número de folds entre 5 e 10, e o número de árvore entre 1, 5, 10, 25, 50, 75 e 100. Os resultados dos experimentos são exportados para um arquivo csv na pasta results para cada dataset diferente de entrada presente na pasta dataset.

Para executar:
``` sh
  ./main.py
```

Or:

```
  python3 ./main.py
```


### Dependências:

* Python >= v3.8
