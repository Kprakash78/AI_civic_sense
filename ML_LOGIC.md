***

### 3. `ML_LOGIC.md` (Intelligence & Decision Layer)

```markdown
# ML Logic & Priority Engine Rules

## 1. Domain Separation
The `/ml` directory strictly handles mathematical modeling and NLP. It does not touch the database, API routes, or HTTP requests. It exposes pure Python functions.

## 2. Severity Model (Danger Detection)
* **Input:** Cleaned text string.
* **Output:** Float $\in [0, 1]$ and SHAP explanation dict.
* **Behavior:** 1.0 indicates immediate threat to life or infrastructure. 0.0 indicates a benign or informational request.

## 3. Credibility Model (Hybrid Approach)
A pure ML approach is vulnerable to adversarial spam. We utilize a Hybrid mechanism.
* **Base ML Score:** NLP evaluation of structural coherence and detail richness.
* **Rule-Based Penalties:**
    * *ALL CAPS SPAM:* Reduce score by $0.3$.
    * *High Frequency:* If IP/User submits > 5 times in 10 minutes, cap score at $0.1$.
    * *Short Length:* If word count < 4, reduce score by $0.4$.
* **Output:** Float $\in [0, 1]$.

## 4. The Priority Engine (System Brain)
The Backend Service Layer imports the ML functions and calculates the final `priority_score`.

**Standard Weighting Formula:**
$$P = (w_s \times S) + (w_c \times C)$$
Where $S$ is Severity, $C$ is Credibility, $w_s = 0.7$, and $w_c = 0.3$.

**Emergency Override Rule:**
If $S > 0.85$, bypass standard weighting. Hardcode $P = 0.95$ and append `"weight_profile_used": "Emergency Override"` to the explanation JSON.

**Priority Label Mapping:**
* $P \ge 0.80$ : `CRITICAL`
* $0.60 \le P < 0.80$ : `HIGH`
* $0.35 \le P < 0.60$ : `MEDIUM`
* $P < 0.35$ : `LOW`

## 5. Explainability Payload Format
The engine must merge outputs from the ML layer into a strict JSON format for the UI to consume:
```json
{
  "severity_reason": "String derived from top SHAP values",
  "credibility_reason": "String detailing ML confidence and any rule penalties applied",
  "weight_profile_used": "Standard | Emergency Override"
}