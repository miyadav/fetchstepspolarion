# Test Steps Redundancy Analysis Report

- **Work items analyzed:** 42
- **Similar pairs found:** 14
- **Redundancy clusters:** 4
- **Unique (no overlap):** 25

---

## Redundancy Clusters

Work items grouped together share significant step overlap and could
potentially be consolidated or have one removed.

### Cluster 1: OCP-23144, OCP-23143, OCP-23017

  - **OCP-23144** (6 steps): Create remote cluster by running:<br/> export CLUSTER_NAME=&quot;qe-olnester&quot;<br/> export SSH_P...
  - **OCP-23143** (8 steps): Create cluster deployment <br/> export CLUSTER_NAME=&quot;<span style="font-weight: bold;">qe-olnest...
  - **OCP-23017** (2 steps): Create cluster deployment with overriden CLUSTER_IMAGE_SET parameter<br/> <br/> export CLUSTER_NAME=...

### Cluster 2: OCP-88225, OCP-88193, OCP-84265

  - **OCP-88225** (9 steps): <span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &#39;Segoe UI&#39;, S...
  - **OCP-88193** (8 steps): <span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &#39;Segoe UI&#39;, S...
  - **OCP-84265** (48 steps): <span style="font-weight: bold;">(PASS)Case 1 - Test with the old format in CD.spec.platform.vsphere...

### Cluster 3: OCP-78223, OCP-78085

  - **OCP-78223** (16 steps): A: Create cluster with <span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family...
  - **OCP-78085** (18 steps): <span style="font-weight: bold;font-style: italic;color: #000000;">Hive version: quay.io/app-sre/hiv...

### Cluster 4: OCP-52465, OCP-52436, OCP-51797, OCP-50936, OCP-50755, OCP-23040, OCP-23101, OCP-29670, OCP-28631

  - **OCP-52465** (12 steps): Create a cluster use <span style="font-weight: bold;color: #24292F;">gen1</span><span style="color: ...
  - **OCP-52436** (10 steps): <span style="font-size: 10pt;line-height: 1.5;">git reset --hard c40aa3421f4c6bdf8a588a7ca3b578efc0d...
  - **OCP-51797** (10 steps): Deploy a clusterdeployment on Alibaba and wait until finish,run :<br/> <br/> <span style="font-size:...
  - **OCP-50936** (10 steps): 1.$ git reset --hard 1566d49af21982b916eaafa166460f3f5ca29764<br/> $ IMG=quay.io/lwan0/hive:1566d49 ...
  - **OCP-50755** (10 steps): 1.Use this IMG to deploy hive on an ocp cluster.<br/> <br/> $ <span style="font-size: 10pt;line-heig...
  - **OCP-23040** (7 steps): <span style="font-size: 10pt;line-height: 1.5;">Login to the hive cluster and create cluster deploym...
  - **OCP-23101** (7 steps): <span style="font-size: 10pt;line-height: 1.5;">Deploy cluster and wait for finish:<br/> $export CLU...
  - **OCP-29670** (6 steps): <span style="font-size: 10pt;line-height: 1.5;">1.Install hive-operator<br/> <span style="text-decor...
  - **OCP-28631** (8 steps): <span style="font-size: 10pt;line-height: 1.5;">1. Deploy a clusterdeployment,run :<br/> $./bin/hive...

---

## Detailed Pair Analysis

Pairs ranked by combined similarity score (text + keyword + step-level).

### 1. OCP-88225 vs OCP-88193

| Metric | Score |
|--------|-------|
| **Combined** | **58.3%** |
| Text similarity | 21.0% |
| Keyword overlap | 70.6% |
| Step-level match | 77.8% (7/8 steps) |

**Verdict:** HIGH — strong candidate to merge or remove one

**Matched steps (OCP-88225 -> OCP-88193):**

- Step 3 (77%): `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
  matches Step 3: `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
- Step 4 (87%): `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
  matches Step 8: `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
- Step 5 (88%): `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
  matches Step 5: `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
- Step 6 (90%): `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
  matches Step 5: `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
- Step 7 (84%): `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
  matches Step 5: `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
- Step 8 (99%): `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
  matches Step 8: `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
- Step 9 (76%): `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
  matches Step 5: `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`

### 2. OCP-23040 vs OCP-28631

| Metric | Score |
|--------|-------|
| **Combined** | **43.0%** |
| Text similarity | 34.9% |
| Keyword overlap | 50.0% |
| Step-level match | 42.9% (3/7 steps) |

**Verdict:** HIGH — strong candidate to merge or remove one

**Matched steps (OCP-23040 -> OCP-28631):**

- Step 3 (62%): `<span style="font-size: 10pt;line-height: 1.5;">add this template to the cluster...`
  matches Step 2: `<span style="font-size: 10pt;line-height: 1.5;">2.Wait until clusterdeployment w...`
- Step 5 (57%): `<span style="font-size: 10pt;line-height: 1.5;">Login to the remote cluster, whi...`
  matches Step 2: `<span style="font-size: 10pt;line-height: 1.5;">2.Wait until clusterdeployment w...`
- Step 6 (56%): `<span style="font-size: 10pt;line-height: 1.5;">Run &quot;oc get configmap&quot;...`
  matches Step 4: `<span style="font-size: 10pt;line-height: 1.5;">4. Check modified is successful,...`

### 3. OCP-23144 vs OCP-23143

| Metric | Score |
|--------|-------|
| **Combined** | **39.9%** |
| Text similarity | 9.4% |
| Keyword overlap | 22.6% |
| Step-level match | 83.3% (6/6 steps) |

**Verdict:** MEDIUM — review for partial overlap

**Matched steps (OCP-23144 -> OCP-23143):**

- Step 1 (60%): `Create remote cluster by running:<br/> export CLUSTER_NAME=&quot;qe-olnester&quo...`
  matches Step 1: `Create cluster deployment <br/> export CLUSTER_NAME=&quot;<span style="font-weig...`
- Step 2 (64%): `Create template for configmap configmap.yaml:<br/> apiVersion: v1<br/> kind: Con...`
  matches Step 7: `Delete next data:<br/> <span style="color: #FF0000;"> - kind: ConfigMap<br/> api...`
- Step 3 (78%): `Go to the remote cluster and run <span style="font-weight: bold;">&quot;oc creat...`
  matches Step 8: `Go to the remote cluster and check results: run &quot;<span style="font-weight: ...`
- Step 5 (75%): `Run &quot;<span style="font-weight: bold;">oc create -f syncset-patch.yaml</span...`
  matches Step 5: `Run &quot;<span style="font-weight: bold;">oc get configmap</span>&quot;<br/>...`
- Step 6 (88%): `Go to the remote cluster and check results: <span style="font-weight: bold;">&qu...`
  matches Step 8: `Go to the remote cluster and check results: run &quot;<span style="font-weight: ...`

### 4. OCP-51797 vs OCP-23101

| Metric | Score |
|--------|-------|
| **Combined** | **35.0%** |
| Text similarity | 1.1% |
| Keyword overlap | 29.1% |
| Step-level match | 70.0% (7/7 steps) |

**Verdict:** MEDIUM — review for partial overlap

**Matched steps (OCP-51797 -> OCP-23101):**

- Step 2 (64%): `Login to the remote cluster,and check machinesets :<br/> <br/> $ oc get machines...`
  matches Step 6: `Wait a few minutes, check it was applied to remote cluster, Its scale to 3 machi...`
- Step 5 (82%): `Wait a few minutes, check machinesets and nodes created successfully on remote c...`
  matches Step 3: `<span style="font-size: 10pt;line-height: 1.5;">Wait a few minutes, check machin...`
- Step 6 (74%): `<span style="font-weight: bold;">Modify machinepool .spec.replicas to 2</span> a...`
  matches Step 5: `Modify machinepool .spec.replicas to 3 and save. Check modifying is successful, ...`
- Step 7 (74%): `Wait a few minutes, check it was applied to remote cluster, <span style="font-we...`
  matches Step 6: `Wait a few minutes, check it was applied to remote cluster, Its scale to 3 machi...`
- Step 8 (75%): `Modify machinepool .spec.replicas to <span style="font-weight: bold;">3</span> a...`
  matches Step 5: `Modify machinepool .spec.replicas to 3 and save. Check modifying is successful, ...`
- Step 9 (80%): `Wait a few minutes, check it was applied to remote cluster, It <span style="font...`
  matches Step 6: `Wait a few minutes, check it was applied to remote cluster, Its scale to 3 machi...`
- Step 10 (57%): `<span style="font-weight: bold;">Delete machinepool created above</span>. Check ...`
  matches Step 6: `Wait a few minutes, check it was applied to remote cluster, Its scale to 3 machi...`

### 5. OCP-23040 vs OCP-29670

| Metric | Score |
|--------|-------|
| **Combined** | **31.5%** |
| Text similarity | 12.1% |
| Keyword overlap | 22.6% |
| Step-level match | 57.1% (4/6 steps) |

**Verdict:** MEDIUM — review for partial overlap

**Matched steps (OCP-23040 -> OCP-29670):**

- Step 3 (55%): `<span style="font-size: 10pt;line-height: 1.5;">add this template to the cluster...`
  matches Step 5: `<span style="font-size: 10pt;line-height: 1.5;">5.Verify Hive&#39;s pods are cre...`
- Step 5 (58%): `<span style="font-size: 10pt;line-height: 1.5;">Login to the remote cluster, whi...`
  matches Step 5: `<span style="font-size: 10pt;line-height: 1.5;">5.Verify Hive&#39;s pods are cre...`
- Step 6 (56%): `<span style="font-size: 10pt;line-height: 1.5;">Run &quot;oc get configmap&quot;...`
  matches Step 5: `<span style="font-size: 10pt;line-height: 1.5;">5.Verify Hive&#39;s pods are cre...`
- Step 7 (56%): `<span style="font-size: 10pt;line-height: 1.5;">Verify the resource configmap ha...`
  matches Step 3: `<span style="font-size: 10pt;line-height: 1.5;">3.Verify the hive-operator is cr...`

### 6. OCP-78223 vs OCP-78085

| Metric | Score |
|--------|-------|
| **Combined** | **31.5%** |
| Text similarity | 3.4% |
| Keyword overlap | 37.0% |
| Step-level match | 50.0% (8/16 steps) |

**Verdict:** MEDIUM — review for partial overlap

**Matched steps (OCP-78223 -> OCP-78085):**

- Step 4 (56%): `Login to spoke cluster, check the <span style="font-weight: normal;font-style: n...`
  matches Step 16: `Login to spoke cluster, check the infra infra machines/machinesets.<br/>...`
- Step 9 (80%): `Check the machinepool status....`
  matches Step 8: `Check the machinepool pod logs....`
- Step 10 (74%): `Login to spoke cluster, check whether the new machines use IPv4 addresses....`
  matches Step 9: `Login to spoke cluster, check the machines status.<br/>...`
- Step 11 (59%): `<span style="font-weight: normal;font-style: normal;font-size: 10pt;font-family:...`
  matches Step 6: `<span style="font-weight: normal;font-style: normal;font-size: 10pt;font-family:...`
- Step 12 (57%): `Login to spoke cluster, check the <span style="font-weight: normal;font-style: n...`
  matches Step 16: `Login to spoke cluster, check the infra infra machines/machinesets.<br/>...`
- Step 14 (96%): `Login to spoke cluster, check the machine status....`
  matches Step 9: `Login to spoke cluster, check the machines status.<br/>...`
- Step 15 (56%): `<span style="font-weight: normal;font-style: normal;font-size: 10pt;font-family:...`
  matches Step 6: `<span style="font-weight: normal;font-style: normal;font-size: 10pt;font-family:...`
- Step 16 (57%): `Login to spoke cluster, check the <span style="font-weight: normal;font-style: n...`
  matches Step 16: `Login to spoke cluster, check the infra infra machines/machinesets.<br/>...`

### 7. OCP-23144 vs OCP-23017

| Metric | Score |
|--------|-------|
| **Combined** | **31.3%** |
| Text similarity | 3.7% |
| Keyword overlap | 36.2% |
| Step-level match | 50.0% (1/2 steps) |

**Verdict:** MEDIUM — review for partial overlap

**Matched steps (OCP-23017 -> OCP-23144):**

- Step 1 (76%): `Create cluster deployment with overriden CLUSTER_IMAGE_SET parameter<br/> <br/> ...`
  matches Step 1: `Create remote cluster by running:<br/> export CLUSTER_NAME=&quot;qe-olnester&quo...`

### 8. OCP-88193 vs OCP-84265

| Metric | Score |
|--------|-------|
| **Combined** | **28.6%** |
| Text similarity | 3.7% |
| Keyword overlap | 16.0% |
| Step-level match | 62.5% (5/8 steps) |

**Verdict:** LOW — minor overlap, likely distinct

**Matched steps (OCP-88193 -> OCP-84265):**

- Step 3 (77%): `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
  matches Step 43: `<span style="font-weight: bold;">Test default worker MP with the following steps...`
- Step 5 (71%): `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
  matches Step 44: `<span style="font-weight: bold;">Create infra1 MP and scale up 1 -&gt; 2 later</...`
- Step 6 (69%): `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
  matches Step 44: `<span style="font-weight: bold;">Create infra1 MP and scale up 1 -&gt; 2 later</...`
- Step 7 (68%): `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
  matches Step 44: `<span style="font-weight: bold;">Create infra1 MP and scale up 1 -&gt; 2 later</...`
- Step 8 (72%): `<span style="font-weight: bold;font-style: normal;font-size: 10pt;font-family: &...`
  matches Step 44: `<span style="font-weight: bold;">Create infra1 MP and scale up 1 -&gt; 2 later</...`

### 9. OCP-29670 vs OCP-28631

| Metric | Score |
|--------|-------|
| **Combined** | **28.5%** |
| Text similarity | 7.5% |
| Keyword overlap | 12.5% |
| Step-level match | 62.5% (5/6 steps) |

**Verdict:** LOW — minor overlap, likely distinct

**Matched steps (OCP-28631 -> OCP-29670):**

- Step 2 (66%): `<span style="font-size: 10pt;line-height: 1.5;">2.Wait until clusterdeployment w...`
  matches Step 5: `<span style="font-size: 10pt;line-height: 1.5;">5.Verify Hive&#39;s pods are cre...`
- Step 4 (65%): `<span style="font-size: 10pt;line-height: 1.5;">4. Check modified is successful,...`
  matches Step 5: `<span style="font-size: 10pt;line-height: 1.5;">5.Verify Hive&#39;s pods are cre...`
- Step 5 (59%): `<span style="font-size: 10pt;line-height: 1.5;">5. Delete clusterdeployment just...`
  matches Step 5: `<span style="font-size: 10pt;line-height: 1.5;">5.Verify Hive&#39;s pods are cre...`
- Step 6 (56%): `<span style="font-size: 10pt;line-height: 1.5;">6.Check logs of hive-controller ...`
  matches Step 5: `<span style="font-size: 10pt;line-height: 1.5;">5.Verify Hive&#39;s pods are cre...`
- Step 8 (66%): `<span style="font-size: 10pt;line-height: 1.5;">8.wait several minutes,and check...`
  matches Step 2: `<span style="font-size: 10pt;line-height: 1.5;">2.Watch your operator come up,ru...`

### 10. OCP-52436 vs OCP-23040

| Metric | Score |
|--------|-------|
| **Combined** | **28.3%** |
| Text similarity | 12.3% |
| Keyword overlap | 41.7% |
| Step-level match | 28.6% (2/7 steps) |

**Verdict:** LOW — minor overlap, likely distinct

**Matched steps (OCP-23040 -> OCP-52436):**

- Step 4 (57%): `<span style="font-size: 10pt;line-height: 1.5;">Run &quot;oc get syncset&quot; t...`
  matches Step 1: `<span style="font-size: 10pt;line-height: 1.5;">git reset --hard c40aa3421f4c6bd...`
- Step 5 (55%): `<span style="font-size: 10pt;line-height: 1.5;">Login to the remote cluster, whi...`
  matches Step 1: `<span style="font-size: 10pt;line-height: 1.5;">git reset --hard c40aa3421f4c6bd...`

### 11. OCP-23040 vs OCP-23101

| Metric | Score |
|--------|-------|
| **Combined** | **28.1%** |
| Text similarity | 34.0% |
| Keyword overlap | 22.7% |
| Step-level match | 28.6% (2/7 steps) |

**Verdict:** LOW — minor overlap, likely distinct

**Matched steps (OCP-23101 -> OCP-23040):**

- Step 1 (70%): `<span style="font-size: 10pt;line-height: 1.5;">Deploy cluster and wait for fini...`
  matches Step 1: `<span style="font-size: 10pt;line-height: 1.5;">Login to the hive cluster and cr...`
- Step 4 (80%): `<span style="font-size: 10pt;line-height: 1.5;">Check machineset has label &quot...`
  matches Step 7: `<span style="font-size: 10pt;line-height: 1.5;">Verify the resource configmap ha...`

### 12. OCP-52436 vs OCP-50755

| Metric | Score |
|--------|-------|
| **Combined** | **27.4%** |
| Text similarity | 12.5% |
| Keyword overlap | 7.6% |
| Step-level match | 60.0% (6/10 steps) |

**Verdict:** LOW — minor overlap, likely distinct

**Matched steps (OCP-50755 -> OCP-52436):**

- Step 1 (61%): `1.Use this IMG to deploy hive on an ocp cluster.<br/> <br/> $ <span style="font-...`
  matches Step 1: `<span style="font-size: 10pt;line-height: 1.5;">git reset --hard c40aa3421f4c6bd...`
- Step 5 (60%): `5.Check cd&#39;s <span style="font-size: 10pt;line-height: 1.5;">condition again...`
  matches Step 8: `Check pod&#39;s log of <span style="font-size: 10pt;line-height: 1.5;">controlle...`
- Step 7 (60%): `7. Check cd&#39;s <span style="font-size: 10pt;line-height: 1.5;">condition agai...`
  matches Step 8: `Check pod&#39;s log of <span style="font-size: 10pt;line-height: 1.5;">controlle...`
- Step 8 (55%): `<br/> <span style="font-size: 10pt;line-height: 1.5;">8.Update the latest versio...`
  matches Step 1: `<span style="font-size: 10pt;line-height: 1.5;">git reset --hard c40aa3421f4c6bd...`
- Step 9 (60%): `9. Check cd&#39;s <span style="font-size: 10pt;line-height: 1.5;">condition agai...`
  matches Step 8: `Check pod&#39;s log of <span style="font-size: 10pt;line-height: 1.5;">controlle...`
- Step 10 (59%): `<span style="font-size: 10pt;line-height: 1.5;">10. Wait for CDs provisioned and...`
  matches Step 1: `<span style="font-size: 10pt;line-height: 1.5;">git reset --hard c40aa3421f4c6bd...`

### 13. OCP-52465 vs OCP-51797

| Metric | Score |
|--------|-------|
| **Combined** | **26.6%** |
| Text similarity | 0.9% |
| Keyword overlap | 15.3% |
| Step-level match | 60.0% (6/10 steps) |

**Verdict:** LOW — minor overlap, likely distinct

**Matched steps (OCP-51797 -> OCP-52465):**

- Step 2 (87%): `Login to the remote cluster,and check machinesets :<br/> <br/> $ oc get machines...`
  matches Step 2: `Login to the remote cluster,and check machinesets :<br/> $hack/get-kubeconfig.sh...`
- Step 4 (100%): `<span style="font-size: 10pt;line-height: 1.5;">Check machinepool CRD created su...`
  matches Step 4: `<span style="font-size: 10pt;line-height: 1.5;">Check machinepool mihuang1696-os...`
- Step 5 (98%): `Wait a few minutes, check machinesets and nodes created successfully on remote c...`
  matches Step 6: `Wait a few minutes, check machinesets and nodes created successfully on remote c...`
- Step 7 (100%): `Wait a few minutes, check it was applied to remote cluster, <span style="font-we...`
  matches Step 8: `Wait a few minutes, check it was applied to remote cluster, <span style="font-we...`
- Step 9 (99%): `Wait a few minutes, check it was applied to remote cluster, It <span style="font...`
  matches Step 10: `Wait a few minutes, check it was applied to remote cluster, It <span style="font...`
- Step 10 (100%): `<span style="font-weight: bold;">Delete machinepool created above</span>. Check ...`
  matches Step 11: `<span style="font-weight: bold;">Delete machinepool created above</span>. Check ...`

### 14. OCP-50936 vs OCP-23040

| Metric | Score |
|--------|-------|
| **Combined** | **25.4%** |
| Text similarity | 2.6% |
| Keyword overlap | 13.2% |
| Step-level match | 57.1% (4/7 steps) |

**Verdict:** LOW — minor overlap, likely distinct

**Matched steps (OCP-23040 -> OCP-50936):**

- Step 3 (58%): `<span style="font-size: 10pt;line-height: 1.5;">add this template to the cluster...`
  matches Step 5: `5.<span style="font-size: 10pt;line-height: 1.5;">Upgrade hive version<br/> $ gi...`
- Step 4 (56%): `<span style="font-size: 10pt;line-height: 1.5;">Run &quot;oc get syncset&quot; t...`
  matches Step 3: `3.Check the <span style="font-size: 10pt;line-height: 1.5;">Controller&#39;s log...`
- Step 5 (60%): `<span style="font-size: 10pt;line-height: 1.5;">Login to the remote cluster, whi...`
  matches Step 6: `<span style="font-size: 10pt;line-height: 1.5;">6.Check if the machinepool is cr...`
- Step 6 (59%): `<span style="font-size: 10pt;line-height: 1.5;">Run &quot;oc get configmap&quot;...`
  matches Step 6: `<span style="font-size: 10pt;line-height: 1.5;">6.Check if the machinepool is cr...`

---

## Recommendations

### Merge or Remove (HIGH similarity)

- **OCP-88225** and **OCP-88193** (58% similar): `OCP-88193` is a subset of `OCP-88225` — consider removing `OCP-88193` or merging its unique steps into `OCP-88225`.
- **OCP-23040** and **OCP-28631** (43% similar): `OCP-23040` is a subset of `OCP-28631` — consider removing `OCP-23040` or merging its unique steps into `OCP-28631`.

### Review for Partial Consolidation (MEDIUM similarity)

- **OCP-23144** and **OCP-23143** (40% similar): share overlapping setup/verification steps — extract shared steps into a common precondition or reference one from the other.
- **OCP-51797** and **OCP-23101** (35% similar): share overlapping setup/verification steps — extract shared steps into a common precondition or reference one from the other.
- **OCP-23040** and **OCP-29670** (32% similar): share overlapping setup/verification steps — extract shared steps into a common precondition or reference one from the other.
- **OCP-78223** and **OCP-78085** (31% similar): share overlapping setup/verification steps — extract shared steps into a common precondition or reference one from the other.
- **OCP-23144** and **OCP-23017** (31% similar): share overlapping setup/verification steps — extract shared steps into a common precondition or reference one from the other.

### No Action Needed

25 work items show no significant overlap with any other and should be kept as-is.

