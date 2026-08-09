# 📚 Documento 04: Referencias Bibliográficas, Marco Normativo y Fundamentos Matemáticos

**Proyecto:** SkyRoute Drones - Sistema Integrado de Telemetría, Logística y Tráfico Aéreo UAS  
**Asignatura:** Algoritmos de Programación Orientada a Objetos (UDEM)  

---

## 1. Fundamentos Matemáticos: Fórmula de Haversine
Para calcular la distancia más corta sobre la superficie de una esfera (distancia ortodrómica) entre dos puntos geográficos especificados por su latitud ($\phi$) y longitud ($\lambda$), se utiliza la **Fórmula de Haversine**:

$$\Delta \phi = \phi_2 - \phi_1$$
$$\Delta \lambda = \lambda_2 - \lambda_1$$
$$a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1) \cdot \cos(\phi_2) \cdot \sin^2\left(\frac{\Delta \lambda}{2}\right)$$
$$c = 2 \cdot \operatorname{atan2}\left(\sqrt{a}, \sqrt{1-a}\right)$$
$$d = R \cdot c$$

Donde:
* $R = 6371.0 \text{ km}$ (Radio medio de la Tierra).
* $\phi_1, \phi_2$ son las latitudes expresadas en radianes.
* $d$ es la distancia en kilómetros entre origen y destino.

---

## 2. Marco Normativo Regulatorio Aeronáutico
1. **UAEAC (Unidad Administrativa Especial de Aeronáutica Civil - Colombia):**
   * **Reglamento Aeronáutico de Colombia (RAC 91 / RAC 100):** Establece que las operaciones no recreativas de aeronaves pilotadas a distancia (SART / UAS) deben operar por debajo de los **120 metros (400 pies) AGL**.
   * **Geofencing:** Prohibición estricta de sobrevuelo en un radio de 5 km alrededor de aeropuertos comerciales o zonas militares.
2. **FAA (Federal Aviation Administration - EE. UU.):**
   * **Small UAS Rule (Part 107):** Regula el peso máximo de despegue ($< 25\text{ kg}$) y la obligación de contar con alertas de batería baja para aterrizaje preventivo.

---

## 3. Referencias Bibliográficas Técnicas
1. **Van Rossum, G., Drake, F. L., & FL, D.** (2009). *Python 3 Reference Manual*. CreateSpace.
2. **Sinnott, R. W.** (1984). *Virtues of the Haversine*. Sky and Telescope, 68(2), 159.
3. **Aeronáutica Civil de Colombia.** (2021). *RAC 100 - Operación de Sistemas de Aeronaves No Tripuladas (UAS)*. Bogotá D.C.
4. **Gamma, E., Helm, R., Johnson, R., & Vlissides, J.** (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
