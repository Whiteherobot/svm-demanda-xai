# Máquinas de Soporte Vectorial (SVM) — Entregables

**Michael Lata · Técnicas de ML Supervisado**

Trabajo sobre SVM: investigación teórica, implementación en código, aplicación a un
caso real de negocio (**predicción de demanda**, dataset de la Práctica 2) y
explicabilidad (XAI).

## Estructura

```
.
├── 1_Informe/                  Informe teórico
│   ├── informe.pdf             · PDF final
│   └── informe.tex             · fuente LaTeX
├── 2_Notebooks/                Cuadernos (ejecutados, con salidas y gráficos)
│   ├── SVM_implementacion.ipynb          · teoría del informe llevada a código
│   ├── 01_Modelado_SVM_Demanda.ipynb     · aplicación: SVR de demanda (dataset Práctica 2)
│   ├── 02_XAI_SVM_Demanda.ipynb          · explicabilidad (permutación, PDP, SHAP)
│   ├── 03_Pasos_Explicacion_SVM.ipynb    · explicación PASO A PASO (lenguaje sencillo, base para diapos)
│   └── artefactos/                       · modelos + datos compartidos entre notebooks
├── 3_Presentacion/
│   └── Presentacion_SVM_Demanda.pptx     · presentación editable (5 diapositivas)
└── 4_PDF_entregar/             TODO en PDF, listo para subir
    ├── 0_Informe_SVM.pdf
    ├── 1_SVM_implementacion.pdf
    ├── 2_Modelado_SVM_Demanda.pdf
    ├── 3_XAI_SVM_Demanda.pdf
    ├── 4_Presentacion_SVM_Demanda.pdf
    └── 5_Pasos_Explicacion_SVM.pdf
```

## Checklist de entregables

- [x] **Informe** sobre SVM (definición, margen, kernel, dual y **proceso interno de
      los vectores de soporte**: KKT, tipos de SV, reconstrucción de w/b/f(x)).
- [x] **Cuaderno de implementación** del informe (verificación numérica del proceso
      interno de los vectores de soporte).
- [x] **Cuaderno de aplicación — Modelado SVM para predicción de demanda**: usa el
      dataset de la **Práctica 2**, replica sus 12 features y compara contra sus
      métricas. **El SVR supera al modelo de la práctica** (R² 0.42 vs 0.28; RMSE 5.1
      vs 7.1) y añade una alerta de alta demanda con SVC.
- [x] **Cuaderno de aplicación — XAI para SVM** (permutation importance, PDP, SHAP
      global y local) → factores que impulsan la demanda.
- [x] **Cuaderno paso a paso** (`03_Pasos_Explicacion_SVM.ipynb`): explica en lenguaje
      sencillo cómo entran los datos, el filtro de escala, cómo decide la SVM y **por qué
      la predicción es buena** → base directa para armar las diapositivas.
- [x] **Presentación** (máximo 5 diapositivas).
- [x] **Todo exportado a PDF** (carpeta `4_PDF_entregar/`).

## Idea central

Sobre un dataset real de negocio con **pocos datos**, la **SVM/SVR iguala y supera** a
modelos más complejos (LSTM/boosting de la Práctica 2) siendo **determinista, ligera,
sin GPU y explicable** → la opción más práctica y atractiva para una empresa.

## Entorno

- venv `cv-ai311` (Python 3.11). Librerías: scikit-learn, shap, matplotlib, pandas,
  python-pptx.
- Datos: `Practica_2/data/sales_history.csv` (los notebooks lo leen por ruta absoluta).
- Para reejecutar los notebooks, hacerlo desde la carpeta `2_Notebooks/`
  (las rutas a `artefactos/` son relativas).

## Licencia

MIT. Ver [LICENSE](LICENSE).
