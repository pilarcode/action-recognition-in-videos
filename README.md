# Action Recognition in videos 

## Overview 
Mi **Trabajo fin de Máster** sobre el reconocimiento de acciones en los videos sobre un dominio concreto, el baile. 
En primer lugar, se entrenan dos modelos con dos enfoques diferentes utilizando el dataset de [Let's Dance](https://www.cc.gatech.edu/cpl/projects/dance/)

![Dataset ejemplos](https://www.cc.gatech.edu/cpl/projects/dance/img/paper_figure.png)

En segundo lugar, se implementa una API con dos servicios, un servicio para testear cada modelo con videos no vistos por el modelo. Cada servicio recibe una url y devuelve un json con la etiqueta y la confianza del modelo para cada clase posible.

![inferencia ejemplos](https://github.com/pilarcode/action-recognition-in-videos/blob/master/images/ejemplo_inferencia.png)

## Notes 
El primer modelo usa transfer learning sobre un modelo pre-entrenado. El segundo modelo fue entrenado creando una red convolucional usando filtros convolucionales 3D para reconocer las características espacio-temporales en una secuencia de frames. Estos fueron los resultados obtenidos y las condiciones de entrenamiento.

![table 1](https://github.com/pilarcode/action-recognition-in-videos/blob/master/images/table1.png)

![table 1](https://github.com/pilarcode/action-recognition-in-videos/blob/master/images/table2.png)

**References**:
Castro, D. (2018, January 23). Let’s Dance: Learning From Online Dance Videos. ArXiv.Org. https://arxiv.org/abs/1801.07388 

