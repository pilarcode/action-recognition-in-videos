# Action Recognition in videos 

## Overview 
Mi **Trabajo fin de Máster** sobre el reconocimiento de acciones en los videos sobre un dominio concreto, el baile. 
En primer lugar, se entrenan dos modelos con dos approaches diferentes detallados en el paper del proyecto utilizando el dataset de [Let's Dance](https://www.cc.gatech.edu/cpl/projects/dance/)

![Dataset ejemplos](https://www.cc.gatech.edu/cpl/projects/dance/img/paper_figure.png)

En segundo lugar, se implementa una API con dos servicios uno para cada modelo. Cada servicio recibe una url y devuelve un json con la etiqueta y la confianza del modelo para cada clase posible.

![inferencia ejemplos](https://github.com/pilarcode/action-recognition-in-videos/blob/master/images/ejemplo_inferencia.png)

## Notes 
El primer modelo se entreno aplicando transfer learning sobre un modelo ya pre-entrenado y el segundo modelo se entrenó desde cero aplicando filtros convolucionales 3D para reconocer las características espacio-temporales.

![table 1](https://github.com/pilarcode/action-recognition-in-videos/blob/master/images/table1.png)

![table 1](https://github.com/pilarcode/action-recognition-in-videos/blob/master/images/table2.png)

**References**:
Castro, D. (2018, January 23). Let’s Dance: Learning From Online Dance Videos. ArXiv.Org. https://arxiv.org/abs/1801.07388 

