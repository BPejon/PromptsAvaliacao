# 3D Object Detection for Autonomous Driving: A Comprehensive Survey

**Abstract** Autonomous driving, in recent years, has been receiving increasing attention for its potential to relieve drivers' burdens and improve the safety of driving. In modern autonomous driving pipelines, the perception system is an indispensable component, aiming to accurately estimate the status of surrounding environments and provide reliable observations for prediction and planning. 3D object detection, which aims to predict the locations, sizes, and categories of the 3D objects near an autonomous vehicle, is an important part of a perception system. This paper reviews the advances in 3D object detection for autonomous driving. First, we introduce the background of 3D object detection and discuss the challenges in this task. Second, we conduct a comprehensive survey of the progress in 3D object detection from the aspects of models and sensory inputs, including LiDAR-based, camera-based, and multi-modal detection approaches. We also provide an in-depth analysis of the potentials and challenges in each category of methods. Additionally, we systematically investigate the applications of 3D object detection in driving systems. Finally, we conduct a performance analysis of the 3D object detection approaches, and we further summarize the research trends over the years and prospect the future directions of this area.

**Keywords** 3D object detection · perception · autonomous driving · deep learning · computer vision · robotics

## 1 Introduction

Autonomous driving, which aims to enable vehicles to perceive the surrounding environments intelligently and move safely with little or no human effort, has attained rapid progress in recent years. Autonomous driving techniques have been broadly applied in many scenarios, including self-driving trucks, robotaxis, delivery robots, etc., and are capable of reducing human error and enhancing road safety. As a core component of autonomous driving systems, automotive perception helps autonomous vehicles understand the surrounding environments with sensory input. Perception systems generally take multi-modality data (images from cameras, point clouds from LiDAR scanners, high-definition maps etc.) as input, and predict the geometric and semantic information of critical elements on a road. High-quality perception results serve as reliable observations for the following steps such as object tracking, trajectory prediction, and path planning.

To obtain a comprehensive understanding of driving environments, many vision tasks can be involved in a perception system, e.g. object detection and tracking, lane detection, and semantic and instance segmentation. Among these perception tasks, 3D object detection is one of the most indispensable tasks in an automotive perception system. 3D object detection aims to predict the locations, sizes, and classes of critical objects, e.g. cars, pedestrians, cyclists, in the 3D space. In contrast to 2D object detection which only generates 2D bounding boxes on images and ignores the actual distance information of objects from the ego-vehicle, 3D object detection focuses on the localization and recognition of objects in the real-world 3D coordinate system. The geometric information predicted by 3D object detection in real-world coordinates can be directly utilized to measure the distances between the ego-vehicle and critical objects, and to further help plan driving routes and avoid collisions.

3D object detection methods have evolved rapidly with the advances of deep learning techniques in computer vision and robotics. These methods have been trying to address the 3D object detection problem from a particular aspect, e.g. detection from a particular sensory type or data representation, and lack a systematic comparison with the methods of other categories. Hence a comprehensive analysis of the strengths and weaknesses of all types of 3D object detection methods is desirable and can provide some valuable findings to the research community.

To this end, we propose to comprehensively review the 3D object detection methods for autonomous driving applications and provide in-depth analysis and a systematic comparison on different categories of approaches. Compared to the existing surveys [5, 151, 232], our paper broadly covers the recent advances in this area, e.g. 3D object detection from range images, self-/semi-/weakly-supervised 3D object detection, 3D detection in end-to-end driving systems. In contrast to the previous surveys that only focus on detection from point cloud [90, 75, 360], from monocular images [317, 179], and from multi-modal inputs [303], our paper systematically investigate the 3D object detection methods from all sensory types and in most application scenarios. The major contributions of this work can be summarized as follows:

We provide a comprehensive review of the 3D object detection methods from different perspectives, including detection from different sensory inputs (LiDAR-based, camera-based, and multi-modal detection), detection from temporal sequences, label-efficient detection, as well as the applications of 3D object detection in driving systems. We summarize 3D object detection approaches structurally and hierarchically, conduct a systematic analysis of these methods, and provide valuable insights for the potentials and challenges of different categories of methods. We conduct a comprehensive performance and speed analysis on the 3D object detection approaches, identify the research trends over years, and provide insightful views on the future directions of 3D object detection.

The structure of this paper is organized as follows. First, we introduce the problem definition, datasets, and evaluation metrics of 3D object detection in Section 2. Then, we review and analyze the 3D object detection methods based on LiDAR sensors (Section 3), cameras (Section 4), multi-sensor fusion (Section 5), and Transformer-based architectures (Section 6). Next, we introduce the detection methods that leverage temporal data in Section 7 and utilize fewer labels in Section 8. We subsequently discuss some critical problems of 3D object detection in driving systems in Section 9. Finally, we conduct a speed and performance analysis, investigate the research trends, and prospect the future directions of 3D object detection in Section 10. A hierarchically-structured taxonomy is shown in Figure 1. We also provide a constantly updated project page here.

Fig. 1: Hierarchically-structured taxonomy of 3D object detection for autonomous driving.

## 2 Background

### 2.1 What is 3D object detection?

**Problem definition.** 3D object detection aims to predict bounding boxes of 3D objects in driving scenarios from sensory inputs. A general formula of 3D object detection can be represented as

$$
\mathcal{B} = f_{det}(\mathcal{I}_{sensor}), \quad (1)
$$

where \(\mathcal{B} = \{B*{1},\dots ,B*{N}\}\) is a set of \(N\) 3D objects in a scene, \(f*{det}\) is a 3D object detection model, and \(\mathcal{I}*{sensor}\) is one or more sensory inputs. How to represent a 3D object \(B\_{i}\) is a crucial problem in this task, since it determines what 3D information should be provided for the following prediction and planning steps. In most cases, a 3D object is represented as a 3D cuboid that includes this object, that is

$$
B = [x_{c},y_{c},z_{c},l,w,h,\theta ,class], \quad (2)
$$

where \((x*{c},y*{c},z*{c})\) is the 3D center coordinate of a cuboid, \(l,w,h\) is the length, width, and height of a cuboid respectively, \(\theta\) is the heading angle, i.e. the yaw angle, of a cuboid on the ground plane, and class denotes the category of a 3D object, e.g. cars, trucks, pedestrians, cyclists. In [15], additional parameters \(v*{x}\) and \(v\_{y}\) that describe the speed of a 3D object along \(\mathbf{x}\) and \(\mathbf{y}\) axes on the ground are employed.

**Sensory inputs.** There are many types of sensors that can provide raw data for 3D object detection. Among the sensors, radars, cameras, and LiDAR (Light Detection And Ranging) sensors are the three most widely adopted sensory types. Radars have long detection range and are robust to different weather conditions. Due to the Doppler effect, radars could provide additional velocity measurements. Cameras are cheap and easily accessible, and can be crucial for understanding semantics, e.g. the type of traffic sign. Cameras produce images \(\mathcal{I}\_{cam}\in \mathcal{P}^{W\times H\times 3}\) for 3D object detection, where \(W,H\) are the width and height of an image, and each pixel has 3 RGB channels. Albeit cheap, cameras have intrinsic limitations to be utilized for 3D object detection. First, cameras only capture appearance information, and are not capable of directly obtaining 3D structural information about a scene. On the other hand, 3D object detection normally requires accurate localization in the 3D space, while the 3D information, e.g. depth, estimated from images normally has large errors. In addition, detection from images is generally vulnerable to extreme weather and time conditions. Detecting objects from images at night or on foggy days is much harder than detection on sunny days, which leads to the challenge of attaining sufficient robustness for autonomous driving.

As an alternative solution, LiDAR sensors can obtain fine-grained 3D structures of a scene by emitting laser beams and then measuring their reflective information. A LiDAR sensor that emits \(m\) beams and conducts measurements for \(n\) times in one scan cycle can produce a range image \(\mathcal{I}_{range}\in R^{m\times n\times 3}\) where each pixel of a range image contains range \(r\) azimuth \(\alpha\) and inclination \(\phi\) in the spherical coordinate system as well as the reflective intensity. Range images are the raw data format obtained by LiDAR sensors, and can be further converted into point clouds by transforming spherical coordinates into Cartesian coordinates. A point cloud can be represented as \(\mathcal{I}_{point} \in R^{N \times 3}\) , where \(N\) denotes the number of points in a scene, and each point has 3 channels of xyz coordinates. Both range images and point clouds contain accurate 3D information directly acquired by LiDAR sensors. Hence in contrast to cameras, LiDAR sensors are more suitable for detecting objects in the 3D space, and LiDAR sensors are also less vulnerable to time and weather changes. However, LiDAR sensors are much more expensive than cameras, which may limit the applications in driving scenarios. An illustration of 3D object detection is shown in Figure 2.

Fig. 2: An illustration of 3D object detection in autonomous driving scenarios.

**Analysis: comparisons with 2D object detection.** 2D object detection, which aims to generate 2D bounding boxes on images, is a fundamental problem in computer vision. 3D object detection methods have borrowed many design paradigms from the 2D counterparts: proposals generation and refinement, anchors, non maximum suppression, etc. However, from many aspects, 3D object detection is not a naive adaptation of 2D object detection methods to the 3D space. (1) 3D object detection methods have to deal with heterogeneous data representations. Detection from point clouds requires novel operators and networks to handle irregular point data, and detection from both point clouds and images needs special fusion mechanisms. (2) 3D object detection methods normally leverage distinct projected views to generate object predictions. As opposed to 2D object detection methods that detect objects from the perspective view, 3D methods have to consider different views to detect 3D objects, e.g. from the bird's-eye view, point view, and cylindrical view. (3) 3D object detection has a high demand for accurate localization of objects in the 3D space. A decimeter-level localization error can lead to a detection failure of small objects such as pedestrians and cyclists, while in 2D object detection, a localization error of several pixels may still maintain a high Intersection over Union (IoU) between predicted and ground truth bounding boxes. Hence accurate 3D geometric information is indispensable for 3D object detection from either point clouds or images.

**Analysis: comparisons with indoor 3D object detection.** There is also a branch of works [226, 227, 228, 169] on 3D object detection in indoor scenarios. Indoor datasets, e.g. ScanNet [54], SUN RGB-D [265], provide 3D structures of rooms reconstructed from RGB-D sensors and 3D annotations including doors, windows, beds, chairs, etc. 3D object detection in indoor scenes is also based on point clouds or images. However, compared to indoor 3D object detection, there are unique challenges of detection in driving scenarios. (1) Point cloud distributions from LiDAR and RGB-D sensors are different. In indoor scenes, points are relatively uniformly distributed on the scanned surfaces and most 3D objects receive a sufficient number of points on their surfaces. However, in driving scenes most points fall in a near neighborhood of the LiDAR sensor, and those 3D objects that are far away from the sensor will receive only a few points. Thus methods in driving scenarios are specially required to handle various point cloud densities of 3D objects and accurately detect those faraway and sparse objects. (2) Detection in driving scenarios has a special demand for inference latency. Perception in driving scenes has to be real-time to avoid accidents. Hence those methods are required to be computationally efficient, otherwise they will not be applied in real-world applications.

### 2.2 Datasets

A large number of driving datasets have been built to provide multi-modal sensory data and 3D annotations for 3D object detection. Table 1 lists the datasets that collect data in driving scenarios and provide 3D cuboid annotations. KITTI [82] is a pioneering work that proposes a standard data collection and annotation paradigm: equipping a vehicle with cameras and LiDAR sensors, driving the vehicle on roads for data collection, and annotating 3D objects from the collected data. The following works made improvements mainly from the 4 aspects. (1) Increasing the scale of data. Compared to [82], the recent large-scale datasets [268, 15, 186] have more than 10x point clouds, images and annotations. (2) Improving the diversity of data. [82] only contains driving data obtained in the daytime and in good weather, while recent datasets [51, 30, 218, 15, 268, 321, 186, 315] provide data captured at night or in rainy days. (3) Providing more annotated categories. Some datasets [154, 321, 84, 315, 15] can provide more fine-grained object classes, including animals, barriers, traffic cones, etc. They also provide fine-grained sub-categories of existing classes, e.g. the adult and child category of the existing pedestrian class in [15]. (4) Providing data of more modalities. In addition to images and point clouds, recent datasets provide more data types, including high-definition maps [114, 30, 268, 315], radar data [15], long-range LiDAR data [313, 307], thermal images [51].

Table 1: Datasets for 3D object detection in driving scenarios.

| Dataset                | Year | Size (hr.) | Real-world | LiDAR scans | Images | 3D annotations | Classes | night/rain | Locations | Other data       |
| ---------------------- | ---- | ---------- | ---------- | ----------- | ------ | -------------- | ------- | ---------- | --------- | ---------------- |
| KITTI [82, 83]         | 2012 | 1.5        | Yes        | 15k         | 15k    | 200k           | 8       | No/No      | Germany   | -                |
| KAIST [51]             | 2018 | -          | Yes        | 8.9k        | 8.9k   | Yes            | 3       | Yes/No     | Korea     | thermal images   |
| ApolloScape [110, 180] | 2019 | 100        | Yes        | 20k         | 144k   | 475k           | 6       | -/-        | China     | -                |
| H3D [214]              | 2019 | 0.77       | Yes        | 27k         | 83k    | 1.1M           | 8       | No/No      | USA       | -                |
| Lyft L5 [114]          | 2019 | 2.5        | Yes        | 46k         | 323k   | 1.3M           | 9       | No/No      | USA       | maps             |
| Argoverse [30]         | 2019 | 0.6        | Yes        | 44k         | 490k   | 993k           | 15      | Yes/Yes    | USA       | maps             |
| WoodScape [352]        | 2019 | -          | Yes        | 10k         | 10k    | -              | 3       | Yes/Yes    | -         | fish-eye camera  |
| AIODrive [313]         | 2020 | 6.9        | No         | 250k        | 250k   | 26M            | -       | Yes/Yes    | -         | long-range data  |
| A\*3D [218]            | 2020 | 55         | Yes        | 39k         | 39k    | 230k           | 7       | Yes/Yes    | SG        | -                |
| A2D2 [84]              | 2020 | -          | Yes        | 12.5k       | 41.3k  | -              | 14      | -/-        | Germany   | -                |
| Cityscapes 3D [79]     | 2020 | -          | Yes        | 05k         | -      | 8              | No/No   | Germany    | -         |
| nuScenes [15]          | 2020 | 5.5        | Yes        | 400k        | 1.4M   | 1.4M           | 23      | Yes/Yes    | SG, USA   | maps, radar data |
| Waymo Open [268]       | 2020 | 6.4        | Yes        | 230k        | 1M     | 12M            | 4       | Yes/Yes    | USA       | maps             |
| Cirrus [307]           | 2021 | -          | Yes        | 6.2k        | 6.2k   | -              | 8       | -/-        | USA       | long-range data  |
| PandaSet [321]         | 2021 | 0.22       | Yes        | 8.2k        | 49k    | 1.3M           | 28      | Yes/Yes    | USA       | -                |
| KITTI-360 [154]        | 2021 | -          | Yes        | 80k         | 300k   | 68k            | 37      | -/-        | Germany   | -                |
| Argoverse v2 [315]     | 2021 | -          | Yes        | -           | -      | -              | 30      | Yes/Yes    | USA       | maps             |
| ONCE [186]             | 2021 | 144        | Yes        | 1M          | 7M     | 417K           | 5       | Yes/Yes    | China     | -                |

**Analysis: future prospects of driving datasets.** The research community has witnessed an explosion of datasets for 3D object detection in autonomous driving scenarios. A subsequent question may be asked: what will the next-generation autonomous driving datasets look like? Considering the fact that 3D object detection is not an independent task but a component in driving systems, we propose that future datasets will include all important tasks in autonomous driving: perception, prediction, planning, and mapping, as a whole and in an end-to-end manner, so that the development and evaluation of 3D object detection methods will be considered from an overall and systematic view. There are some datasets [268, 15, 352] working towards this goal.

### 2.3 Evaluation metrics

Various evaluation metrics have been proposed to measure the performance of 3D object detection methods. Those evaluation metrics can be divided into two categories. The first category tries to extend the Average Precision (AP) metric [155] in 2D object detection to the 3D space:

$$
AP = \int_{0}^{1}max\{p(r^{\prime}|r^{\prime}\geq r)\} dr, \quad (3)
$$

where \(p(r)\) is the precision-recall curve same as [155]. The major difference with the 2D AP metric lies in the matching criterion between ground truths and predictions when calculating precision and recall. KITTI [82] proposes two widely-used AP metrics: \(AP*{3D}\) and \(AP*{BEV}\) , where \(AP*{3D}\) matches the predicted objects to the respective ground truths if the 3D Intersection over Union (3D IoU) of two cuboids is above a certain threshold, and \(AP*{BEV}\) is based on the IoU of two cuboids from the bird's-eye view (BEV IoU). NuScenes [15] proposes \(AP*{center}\) where a predicted object is matched to a ground truth object if the distance of their center locations is below a certain threshold, and NuScenes Detection Score (NDS) is further proposed to take both \(AP*{center}\) and the error of other parameters, i.e. size, heading, velocity, into consideration. Waymo [268] proposes \(AP\_{hungarian}\) that applies the Hungarian algorithm to match the ground truths and predictions, and AP weighted by Heading (APH) is proposed to incorporate heading errors as a coefficient into the AP calculation.

The other category of approaches tries to resolve the evaluation problem from a more practical perspective. The idea is that the quality of 3D object detection should be relevant to the downstream task, i.e. motion planning, so that the best detection methods should be most helpful to planners to ensure the safety of driving in practical applications. Toward this goal, PKL [220] measures the detection quality using the KL-divergence of the ego vehicle's future planned states based on the predicted and ground truth detections respectively. SDE [56] leverages the minimal distance from the object boundary to the ego vehicle as the support distance and measures the support distance error.

**Analysis: pros and cons of different evaluation metrics.** AP-based evaluation metrics [82, 15, 268] can naturally inherit the advantages from 2D detection. However, those metrics overlook the influence of detection on safety issues, which are also critical in real-world applications. For instance, a misdetection of an object near the ego vehicle and far away from the ego vehicle may receive a similar level of punishment in AP calculation, but a misdetection of nearby objects is substantially more dangerous than a misdetection of faraway objects in practical applications. Thus AP-based metrics may not be the optimal solution from the perspective of safe driving. PKL [220] and SDE [56] partly resolve the problem by considering the effects of detection in downstream tasks, but additional challenges will be introduced when modeling those effects. PKL [220] requires a pre-trained motion planner for evaluating the detection performance, but a pre-trained planner also has innate errors that could make the evaluation process inaccurate. SDE [56] requires reconstructing object boundaries which is generally complicated and challenging.

## 3 LiDAR-based 3D Object Detection

In this section, we introduce the 3D object detection methods based on LiDAR data, i.e. point clouds or range images. In Section 3.1, we review and analyze the LiDAR-based 3D object detection models based on different data representations, including the point-based, grid-based, point-voxel based, and range-based methods. In Section 3.2, we investigate the learning objectives for 3D object detectors, including the anchor-based and anchor-free frameworks, as well as the auxiliary tasks adopted in LiDAR-based 3D object detection. A chronological overview of the LiDAR-based 3D detection methods is shown in Figure 3.

Fig. 3: Chronological overview of the LiDAR-based 3D object detection methods.

Fig. 4: An illustration of point-based 3D object detection methods.

### 3.1 Data representations for 3D object detection

**Problem and Challenge.** In contrast to images where pixels are regularly distributed on an image plane, point cloud is a sparse and irregular 3D representation that requires specially designed models for feature extraction. Range image is a dense and compact representation, but range pixels contain 3D information instead of RGB values. Hence directly applying conventional convolutional networks on range images may not be an optimal solution. On the other hand, detection in autonomous driving scenarios generally has a requirement for real-time inference. Therefore, how to develop a model that could effectively handle point cloud or range image data while maintaining a high efficiency remains an open challenge to the research community.

#### 3.1.1 Point-based 3D object detection

**General Framework.** Point-based 3D object detection methods generally inherit the success of deep learning techniques on point cloud [224, 225, 300, 184] and propose diverse architectures to detect 3D objects directly from raw points. Point clouds are first passed through a point-based backbone network, in which the points are gradually sampled and features are learned by point cloud operators. 3D bounding boxes are then predicted based on the downsampled points and features. A general point-based detection framework is shown in Figure 4 and a taxonomy of point-based detectors is in Table 2. There are two basic components of a point-based 3D object detector: point cloud sampling and feature learning.

Table 2: A taxonomy of point-based detection methods based on point cloud sampling and feature learning.

| Method            | Context Ω  | Sampling S   | Feature F       |
| ----------------- | ---------- | ------------ | --------------- |
| PointRCNN [252]   | Ball Query | FPS          | Set Abstraction |
| IPOD [339]        | Ball Query | Seg.         | Set Abstraction |
| STD [340]         | Ball Query | FPS          | Set Abstraction |
| 3DSSD [342]       | Ball Query | Fusion-FPS   | Set Abstraction |
| Point-GNN [256]   | Ball Query | Voxel        | Graph           |
| StarNet [203]     | Ball Query | Targeted-FPS | Graph           |
| Pointformer [208] | Ball Query | FPS + Refine | Transformer     |

**Point Cloud Sampling.** Farthest Point Sampling (FPS) in PointNet++ [225] has been broadly adopted in point-based detectors, in which the farthest points are sequentially selected from the original point set. PointRCNN [252] is a pioneering work that adopts FPS to progressively downsample input point cloud and generate 3D proposals from the downsampled points. Similar design paradigm has also been adopted in many following works with improvements like segmentation guided filtering [339], feature space sampling [342], random sampling [203], voxel-based sampling [256], and coordinate refinement [208].

**Point Cloud Feature Learning.** A series of works [252, 340, 379, 290] leverage set abstraction in [224] to learn features from point cloud. Specifically, context points are first collected within a pre-defined radius by ball query. Then, the context points and features are aggregated through multi-layer perceptrons and maxpooling to obtain the new features. There are also other works resorting to different point cloud operators, including graph operators [256, 361, 203, 74, 97], attentional operators [205], and Transformer [208].

**Analysis: potentials and challenges on point cloud feature learning and sampling.** The representation power of point-based detectors is mainly restricted by two factors: the number of context points and the context radius adopted in feature learning. Increasing the number of context points will gain more representation power but at the cost of increasing much memory consumption. Suitable context radius in ball query is also an important factor: the context information may be insufficient if the radius is too small and the fine-grained 3D information may lose if the radius is too large. These two factors have to be determined carefully to balance the efficacy and efficiency of detection models.

Point cloud sampling is a bottleneck in inference time for most point-based methods. Random uniform sampling can be conducted in parallel with high efficiency. However, considering points in LiDAR sweeps are not uniformly distributed, random uniform sampling may tend to over-sample those regions of high point cloud density while under-sample those sparse regions, which normally leads to poor performance compared to farthest point sampling. Farthest point sampling and its variants can attain a more uniform sampling result by sequentially selecting the farthest point from the existing point set. Nevertheless, farthest point sampling is intrinsically a sequential algorithm and can not become highly parallel. Thus farthest point sampling is normally time-consuming and not ready for real-time detection.

#### 3.1.2 Grid-based 3D object detection

**General Framework.** Grid-based 3D object detectors first rasterize point clouds into discrete grid representations, i.e. voxels, pillars, and bird's-eye view (BEV) feature maps. Then they apply conventional 2D convolutional neural networks or 3D sparse neural networks to extract features from the grids. Finally, 3D objects can be detected from the BEV grid cells. An illustration of grid-based 3D object detection is shown in Figure 5 and a taxonomy of grid-based detectors is in Table 3. There are two basic components in grid-based detectors: grid-based representations and grid-based neural networks.

Fig. 5: An illustration of grid-based 3D object detection methods.

**Grid-based representations.** There are 3 major types of grid representations: voxels, pillars, and BEV feature maps.

**Voxels.** If we rasterize the detection space into a regular 3D grid, voxels are the grid cells. A voxel can be non-empty if point clouds fall into this grid cell. Since point clouds are sparsely distributed, most voxel cells in the 3D space are empty and contain no point. In practical applications, only those non-empty voxels are stored and utilized for feature extraction. VoxelNet [382] is a pioneering work that utilizes sparse voxel grids and proposes a novel voxel feature encoding (VFE) layer to extract features from the points inside a voxel cell. A similar voxel encoding strategy has been adopted by a series of following works [385, 81, 350, 297, 375, 129, 57, 254]. In addition, there are two categories of approaches trying to improve the voxel representation for 3D object detection: (1) Multi-view voxels. Some methods propose a dynamic voxelization and fusion scheme from diverse views, e.g. from both the bird's-eye view and the perspective view [383], from the cylindrical and spherical view [35], from the range view [59]. (2) Multi-scale voxels. Some papers generate voxels of different scales [344] or use reconfigurable voxels [292].

**Pillars.** Pillars can be viewed as special voxels in which the voxel size is unlimited in the vertical direction. Pillar features can be aggregated from points through a PointNet [224] and then scattered back to construct a 2D BEV image for feature extraction. PointPillars [124] is a seminal work that introduces the pillar representation and is followed by [302, 70].

**BEV feature maps.** Bird's-eye view feature map is a dense 2D representation, where each pixel corresponds to a specific region and encodes the points information in this region. BEV feature maps can be obtained from voxels and pillars by projecting the 3D features into the bird's-eye view, or they can be directly obtained from raw point clouds by summarizing points statistics within the pixel region. The commonly-used statistics include binary occupancy [335, 334, 2] and the height and density of local point cloud [41, 10, 364, 3, 263, 368, 8, 126].

**Grid-based neural networks.** There are 2 major types of grid-based networks: 2D convolutional neural networks for BEV feature maps and pillars, and 3D sparse neural networks for voxels.

**2D convolutional neural networks.** Conventional 2D convolutional neural networks can be applied to the BEV feature map to detect 3D objects from the bird's-eye view. In most works, the 2D network architectures are generally adapted from those successful designs in 2D object detection, e.g. ResNet [95] adopted in [335], Region Proposal Network (RPN) [238] and Feature Pyramid Network (FPN) [156] in [10, 8, 124, 119, 263, 129], and spatial attention in [130, 167, 346].

**3D sparse neural networks.** 3D sparse convolutional neural networks are based on two specialized 3D convolutional operators: sparse convolutions and submanifold convolutions [86], which can efficiently conduct 3D convolutions only on those non-empty voxels. Compared to [283, 68, 201, 125] that perform standard 3D convolutions on the whole voxel space, sparse convolutional operators are highly efficient and can obtain a realtime inference speed. SECOND [333] is a seminal work that implements these two sparse operators with GPU-based hash tables and builds a sparse convolutional network to extract 3D voxel features. This network architecture has been applied in numerous works [385, 350, 347, 297, 81, 36, 388, 333, 57, 375] and becomes the most widely-used backbone network in voxelbased detectors. There is also a series of works trying to improve the sparse operators [49], extend [333] into a two-stage detector [254, 57], and introduce the Transformer [280] architecture into voxel-based detection [187, 70].

Table 3: A taxonomy of grid-based detection methods based on models and data representations.

| Method                  | Voxels | BEV maps | Pillars | Voxelization | Projection | PointNet | 3D CNN | 2D CNN | Head | Transformer |
| ----------------------- | ------ | -------- | ------- | ------------ | ---------- | -------- | ------ | ------ | ---- | ----------- |
| Vote3D [283]            | ✓      |          |         | ✓            |            |          | ✓      |        |      |             |
| Vote3Deep [68]          | ✓      |          |         | ✓            |            |          | ✓      |        |      |             |
| 3D-FCN [125]            | ✓      |          |         | ✓            |            |          | ✓      |        |      |             |
| VeloFCN [126]           |        | ✓        |         |              | ✓          |          |        | ✓      |      |             |
| BirdNet [10]            |        | ✓        |         |              | ✓          |          |        | ✓      |      |             |
| PIXOR [335]             |        | ✓        |         |              | ✓          |          |        | ✓      |      |             |
| HDNet [334]             |        | ✓        |         |              | ✓          |          |        | ✓      |      |             |
| VoxelNet [382]          | ✓      | ✓        |         | ✓            |            | ✓        | ✓      | ✓      |      |             |
| SECOND [333]            | ✓      | ✓        |         | ✓            |            |          | ✓      | ✓      |      |             |
| MVF [383]               | ✓      | ✓        |         | ✓            |            |          |        | ✓      |      |             |
| PointPillars [124]      |        | ✓        | ✓       |              |            | ✓        |        | ✓      |      |             |
| Pillar-OD [302]         |        | ✓        | ✓       |              |            | ✓        |        | ✓      |      |             |
| Part-A2 Net [254]       | ✓      | ✓        |         | ✓            |            |          | ✓      | ✓      | ✓    |             |
| Voxel R-CNN [57]        | ✓      | ✓        |         | ✓            |            |          | ✓      | ✓      | ✓    |             |
| CenterPoint [350]       | ✓      | ✓        |         | ✓            |            |          | ✓      | ✓      |      |             |
| Voxel Transformer [187] | ✓      | ✓        |         | ✓            |            |          |        | ✓      |      | ✓           |
| SST [70]                | ✓      | ✓        |         | ✓            |            |          |        | ✓      |      | ✓           |
| SWFormer [270]          | ✓      | ✓        |         | ✓            |            |          |        |        |      | ✓           |

**Analysis: pros and cons of different grid representations.** In contrast to the 2D representations like BEV feature maps and pillars, voxels contain more structured 3D information. In addition, deep voxel features can be learned through a 3D sparse network. However, a 3D neural network brings additional time and memory costs. BEV feature map is the most efficient grid representation that directly projects point cloud into a 2D pseudo image without specialized 3D operators like sparse convolutions or pillar encoding. 2D detection techniques can also be seamlessly applied to BEV feature maps without much modification. BEV-based detection methods generally can obtain high efficiency and a real-time inference speed. However, simply summarizing points statistics inside pixel regions loses too much 3D information, which leads to less accurate detection results compared to voxel-based detection. Pillar-based detection approaches leverage PointNet to encode 3D points information inside a pillar cell, and the features are then scattered back into a 2D pseudo image for efficient detection, which balances the effectiveness and efficiency of 3D object detection.

**Analysis: challenges of the grid-based detection methods.** A critical problem that all grid-based methods have to face is choosing the proper size of grid cells. Grid representations are essentially discrete formats of point clouds by converting the continuous point coordinates into discrete grid indices. The quantization process inevitably loses some 3D information and its efficacy largely depends on the size of grid cells: smaller grid size yields high resolution grids, and hence maintains more finegrained details that are crucial to accurate 3D object detection. Nevertheless, reducing the size of grid cells leads to a quadratic increase in memory consumption for the 2D grid representations like BEV feature maps or pillars. As for the 3D grid representation like voxels, the problem can become more severe. Therefore, how to balance the efficacy brought by smaller grid sizes and the efficiency influenced by the memory increase remains an open challenge to all grid-based 3D object detection methods.

#### 3.1.3 Point-voxel based 3D object detection

Point-voxel based approaches resort to a hybrid architecture that leverages both points and voxels for 3D object detection. Those methods can be divided into two categories: the single-stage and two-stage detection frameworks. An illustration of the two categories is shown in Figure 6 and a taxonomy is in Table 4.

Fig. 6: An illustration of point-voxel based 3D object detection methods.

**Single-stage point-voxel detection frameworks.** Single-stage point-voxel based 3D object detectors try to bridge the features of points and voxels with the point-to-voxel and voxel-to-point transform in the backbone networks. Points contain fine-grained geometric information and voxels are efficient for computation, and combining them together in the feature extraction stage naturally benefits from both two representations. The idea that leverages point-voxel feature fusion in backbones has been explored by many works, with the contributions like point-voxel convolutions [165, 273], auxiliary point-based networks [94, 131, 58], and multi-scale feature fusion [195, 204, 88].

**Two-stage point-voxel detection frameworks.** Two-stage pointvoxel based 3D object detectors resort to different data representations for different detection stages. Specifically, at the first stage, they employ a voxel-based detection framework to generate a set of 3D object proposals. In the second stage, keypoints are first sampled from the input point cloud, and then the 3D proposals are further refined from the keypoints through novel point operators. PV-RCNN [253] is a seminal work that adopts [333] as the first-stage detector, and the RoI-grid pooling operator is proposed for the second-stage refinement. The following works try to improve the second-stage head with novel modules and operators, e.g. RefinerNet [44], VectorPool [255], point-wise attention [285], scale-aware pooling [144], RoI-grid attention [185], channel-wise Transformer [250], and point density-aware refinement module [101].

Table 4: A taxonomy of point-voxel based detection methods.

| Method                               | Contribution                   |
| ------------------------------------ | ------------------------------ |
| **Single-Stage Detection Framework** |                                |
| PVCNN [165]                          | Point-Voxel Convolution        |
| SPVNAS [273]                         | Sparse Point-Voxel Convolution |
| SA-SSD [94]                          | Auxiliary Point Network        |
| PVGNet [195]                         | Point-Voxel-Grid Fusion        |
| **Two-Stage Detection Framework**    |                                |
| Fast Point R-CNN [44]                | RefinerNet                     |
| PV-RCNN [253]                        | RoI-grid Pooling               |
| PV-RCNN++ [255]                      | VectorPool                     |
| Pyramid R-CNN [185]                  | RoI-grid Attention             |
| LiDAR R-CNN [144]                    | Scale-aware Pooling            |
| CT3D [250]                           | Channel-wise Transformer       |

**Analysis: potentials and challenges of the point-voxel based methods.** The point-voxel based methods can naturally benefit from both the fine-grained 3D shape and structure information obtained from points and the computational efficiency brought by voxels. However, some challenges still exist in these methods. For the hybrid point-voxel backbones, the fusion of point and voxel features generally relies on the voxel-to-point and point-to-voxel transform mechanisms, which can bring non-negligible time costs. For the two-stage point-voxel detection frameworks, a critical challenge is how to efficiently aggregate point features for 3D proposals, as the existing modules and operators are generally time-consuming. In conclusion, compared to the pure voxel-based detection approaches, the point-voxel based detection methods can obtain a better detection accuracy while at the cost of increasing the inference time.

#### 3.1.4 Range-based 3D object detection

Range image is a dense and compact 2D representation in which each pixel contains 3D distance information instead of RGB values. Range-based methods address the detection problem from two aspects: designing new models and operators that are tailored for range images, and selecting suitable views for detection. An illustration of the range-based 3D object detection methods is shown in Figure 7 and a taxonomy is in Table 5.

Fig. 7: An illustration of range-based 3D object detection.

**Range-based detection models.** Since range images are 2D representations like RGB images, range-based 3D object detectors can naturally borrow the models in 2D object detection to handle range images. LaserNet [192] is a seminal work that leverages the deep layer aggregation network (DLA-Net) [356] to obtain multi-scale features and detect 3D objects from range images. Some papers also adopt other 2D object detection architectures, e.g. U-Net [242] is applied in [193, 152, 269], RPN [238] and R-CNN [239] are employed in [152, 11], FCN [171] is used in [153], and FPN [156] is leveraged in [69].

**Range-based operators.** Pixels of range images contain 3D distance information instead of color values, so the standard convolutional operator in conventional 2D network architectures is not optimal for range-based detection, as the pixels in a sliding window may be far away from each other in the 3D space. Some works resort to novel operators to effectively extract features from range pixels, including range dilated convolutions [11], graph operators [27], and meta-kernel convolutions [69].

**Views for range-based detection.** Range images are captured from the range view (RV), and ideally, the range view is a spherical projection of a point cloud. It has been a natural solution for many range-based approaches [192, 11, 69, 27] to detect 3D objects directly from the range view. Nevertheless, detection from the range view will inevitably suffer from the occlusion and scale-variation issues brought by the spherical projection. To circumvent these issues, many methods have been working on leveraging other views for predicting 3D objects, e.g. the cylindrical view (CVY) leveraged in [236], a combination of the range-view, bird's-eye view (BEV), and/or point-view (PV) adopted in [153, 269, 193, 152].

Table 5: A taxonomy of range-based detection methods based on views, models, and operators.

| Method                      | View        | Operator                        | Model            | Note                     |
| --------------------------- | ----------- | ------------------------------- | ---------------- | ------------------------ |
| LaserNet [192]              | RV          | Convolution                     | DLA-Net          | -                        |
| Rapoport-Lavie et al. [236] | RV, CVY     | Convolution                     | Range-Guided Net | -                        |
| LaserFlow [193]             | RV, BEV     | Convolution                     | U-Net            | multi-sweep fusion       |
| RangeRCNN [152]             | RV, PV, BEV | Dilated Convolution             | U-Net, RPN, RCNN | -                        |
| RangeIoUDet [153]           | RV, PV, BEV | Convolution                     | FCN, PointNet    | point-wise segmentation  |
| RCD [11]                    | RV          | Conditioned Dilated Convolution | RPN, RCNN        | -                        |
| RangeDet [69]               | RV          | Meta Kernel Convolution         | FPN              | -                        |
| PPC [27]                    | RV          | Graph Kernel Convolution        | DLA-Net          | -                        |
| RSN [269]                   | RV, BEV     | Convolution                     | U-Net, VoxelNet  | range-based segmentation |

**Analysis: potentials and challenges of the range-based methods.** Range image is a dense and compact 2D representation, so the conventional or specialized 2D convolutions can be seamlessly applied on range images, which makes the feature extraction process quite efficient. Nevertheless, compared to bird's-eye view detection, detection from the range view is vulnerable to occlusion and scale variation. Hence, feature extraction from the range view and object detection from the bird's eye view becomes the most practical solution to range-based 3D object detection.

### 3.2 Learning objectives for 3D object detection

**Problem and Challenge.** Learning objectives are critical in object detection. Since 3D objects are quite small relative to the whole detection range, special mechanisms to enhance the localization of small objects are strongly required in 3D detection. On the other hand, considering point cloud is sparse and objects normally have incomplete shapes, accurately estimating the centers and sizes of 3D objects is a long-standing challenge.

#### 3.2.1 Anchor-based 3D object detection

Anchors are pre-defined cuboids with fixed shapes that can be placed in the 3D space. 3D objects can be predicted based on the positive anchors that have a high intersection over union (IoU) with ground truth. We will introduce the anchor-based 3D object detection methods from the aspect of anchor configurations and loss functions. An illustration of anchor-based learning objectives is shown in Figure 8 and a taxonomy is in Table 6.

Fig. 8: An illustration of anchor-based learning objectives.

**Prerequisites.** The ground truth 3D objects can be represented as \([x^{g},y^{g},z^{g},l^{g},w^{g},h^{g},\theta^{g}]\) with the class \(cls^{g}\) . The anchors \([x^{a},y^{a},z^{a},l^{a},w^{a},h^{a},\theta^{a}]\) are used to generate predicted 3D objects \([x,y,z,l,w,h,\theta ]\) with a predicted class probability \(p\) .

**Anchor configurations.** Anchor-based 3D object detection approaches generally detect 3D objects from the bird's-eye view, in which 3D anchor boxes are placed at each grid cell of a BEV feature map. 3D anchors normally have a fixed size for each category, since objects of the same category have similar sizes.

**Loss functions.** The anchor-based methods employ the classification loss \(L*{cls}\) to learn the positive and negative anchors, and the regression loss \(L*{reg}\) is utilized to learn the size and location of an object based on a positive anchor. Additionally, \(L\_{\theta }\) is applied to learn the object's heading angle. The loss function is

$$
L_{det}=L_{cls}+L_{reg}+L_{\theta }. \quad (4)
$$

VoxelNet [382] is a seminal work that leverages the anchors that have a high IoU with the ground truth 3D objects as positive anchors, and the other anchors are treated as negatives. To accurately classify those positive and negative anchors, for each category, the binary cross entropy loss can be applied to each anchor on the BEV feature map, which can be formulated as

$$
L_{cls}^{bce}=-[q\cdot \log (p)+(1-q)\cdot \log (1-p)], \quad (5)
$$

where \(p\) is the predicted probability for each anchor and the target \(q\) is 1 if the anchor is positive and 0 otherwise. In addition to the binary cross entropy loss, the focal loss [157, 358] has also been employed to enhance the localization ability:

$$
L_{cls}^{focal}=-\alpha (1-p)^{\gamma }\log (p), \quad (6)
$$

where \(\alpha =0.25\) and \(\gamma =2\) are adopted in most works.

The regression targets can be further applied to those positive anchors to learn the sizes and locations of 3D objects:

$$
\begin{array}{l}\Delta x=\frac {x^{g}-x^{a}}{d^{a}},\Delta y=\frac {y^{g}-y^{a}}{d^{a}},\Delta z=\frac {z^{g}-z^{a}}{h^{a}},\\ \Delta l=\log (\frac {l^{g}}{l^{a}}),\Delta w=\log (\frac {w^{g}}{w^{a}}),\Delta h=\log (\frac {h^{g}}{h^{a}})\end{array} \quad (7)
$$

where \(d^{a}=\sqrt {(l^{a})^{2}+(w^{a})^{2}}\) is the diagonal length of an anchor from the bird's-eye view. Then the SmoothL1 loss [239] is adopted to regress the targets, which is represented as

$$
L_{reg}=\sum _{u\in \{x,y,z,l,w,h\},\atop v\in \{x,\Delta y,\Delta z,\Delta l,\Delta w,\Delta h\}}SmoothL1(u-v). \quad (8)
$$

To learn the heading angle \(\theta\) the radian orientation offset can be directly regressed with the SmoothL1 loss:

$$
\begin{array}{l}\Delta \theta = \theta^g -\theta^a,\\ L_{\theta} = \mathrm{SmoothL1}(\theta -\Delta \theta). \end{array} \quad (9)
$$

However, directly regressing the radian offset is normally hard due to the large regression range. Alternatively, the bin-based heading estimation [226] is a better solution to learn the heading angle, in which the angle space is first divided into bins, and bin-based classification \(L\_{dir}\) and residual regression are employed:

$$
L_{\theta} = L_{dir} + \mathrm{SmoothL1}(\theta -\Delta \theta^{\prime}), \quad (10)
$$

where \(\Delta \theta^{\prime}\) is the residual offset within a bin. The sine function can also be utilized to encode the radian offset:

$$
\Delta \theta = \sin (\theta^g -\theta^a), \quad (11)
$$

and \(L^{\theta}\) can be computed following Eqn. 9 or Eqn. 10.

In addition to the loss functions that learn the objects' sizes, locations, and orientations separately, the intersection over union (IoU) loss [378] that considers all object parameters as a whole can also be applied in 3D object detection:

$$
L_{IoU} = 1 - IoU(b^g,b), \quad (12)
$$

where \(b^{g}\) and \(b\) are the ground truth and predicted 3D bounding boxes, and \(IoU(\cdot)\) calculates the 3D IoU in a differential manner. Apart from the IoU loss, the corner loss [226] is also introduced to minimize the distances between the eight corners of the ground truth and predicted boxes, that is

$$
L_{corner} = \sum_{i = 1}^{8}||c_i^g -c_i||, \quad (13)
$$

where \(c*{i}^{g}\) and \(c*{i}\) are the \(i\) th corner of the ground truth and predicted cuboid respectively.

Table 6: A taxonomy of anchor-based methods based on loss functions.

| Loss Function     | Methods                                                                                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lbce (Eqn. 5)     | [263, 3, 10, 364, 382, 8, 340, 339, 44] [97]                                                                                                             |
| Lfocal (Eqn. 6)   | [333, 124, 383, 378, 358, 344, 65, 388] [292, 347, 187, 57, 375, 66, 152, 203] [253, 94, 285, 195, 204, 185, 255]                                        |
| Lreg (Eqn. 8)     | [263, 3, 10, 364, 333, 382, 124, 383, 358] [344, 65, 388, 292, 347, 8, 187, 57] [375, 66, 152, 340, 203, 339, 44, 253] [94, 285, 97, 195, 204, 185, 255] |
| Lθ (Eqn. 9)       | [3, 382, 344, 65, 66, 44]                                                                                                                                |
| Lθ (Eqn. 10)      | [10, 292, 347, 8, 187, 375, 152, 340, 339] [253, 94, 285, 185, 255]                                                                                      |
| Lθ (Eqn. 11)      | [263, 364, 333, 124, 383, 388, 57, 203, 97] [195, 204]                                                                                                   |
| Ltot (Eqn. 12)    | [378]                                                                                                                                                    |
| Lcorner (Eqn. 13) | [344, 152, 340, 339]                                                                                                                                     |

**Analysis: potentials and challenges of the anchor-based approaches.** The anchor-based methods can benefit from the prior knowledge that 3D objects of the same category should have similar shapes, so they can generate accurate object predictions with the help of 3D anchors. However, since 3D objects are relatively small with respect to the detection range, a large number of anchors are required to ensure complete coverage of the whole detection range, e.g. around \(70\mathrm{k}\) anchors are utilized in [333] on the KITTI [82] dataset. Furthermore, for those extremely small objects such as pedestrians and cyclists, applying anchor-based assignments can be quite challenging. Considering the fact that anchors are generally placed at the center of each grid cell, if the grid cell is large and objects in the cell are small, the anchor of this cell may have a low IoU with the small objects, which may hamper the training process.

#### 3.2.2 Anchor-free 3D object detection

Anchor-free approaches eliminate the complicated anchor designs and can be flexibly applied to diverse views, e.g. the bird's-eye view, point view, and range view. An illustration of anchor-free learning objectives is shown in Figure 9 and a taxonomy is in Table 7. The major difference between the anchor-based and anchor-free methods lies in the selection of positive and negative samples. We will introduce the anchor-free methods from the perspective of positive assignments, including grid-based, point-based, range-based, and set-to-set assignments. We still adopt the notations in Section 3.2.1 for simplicity.

Fig. 9: An illustration of anchor-free learning objectives.

**Grid-based assignment.** In contrast to the anchor-based methods that rely on the IoUs with anchors to determine the positive and negative samples, the anchor-free methods leverage various grid-based assignment strategies for BEV grid cells, pillars, and voxels. PIXOR [335] is a pioneering work that leverages the grid cells inside the ground truth 3D objects as positives, and the others as negatives. This inside-object assignment strategy is adopted in [302], and further improved in [81, 103, 36] by selecting the grid cells nearest to the object center. CenterPoint [350] utilizes a Gaussian kernel at each object center to assign positive labels. These methods can still use Eqn. 5 or Eqn. 6 as the classification loss, and the regression target is

$$
\Delta = [dx,dy,z^g,\log (l^g),\log (w^g),\log (h^g),\sin (\theta^g),\cos (\theta^g)],
$$

where \(dx\) and \(dy\) are the offsets between positive grid cells and object centers. The SmoothL1 loss is leveraged to regress \(\Delta\).

**Point-based assignment.** Most point-based detection approaches resort to the anchor-free and point-based assignment strategy, in which the points are first segmented and those foreground points inside or near 3D objects are selected as positive samples, and 3D bounding boxes are finally learned from those foreground points. This foreground point segmentation strategy has been adopted in most point-based detectors [252, 342, 339, 208], with improvements such as adding centerness scores [342], etc.

**Range-based assignment.** Anchor-free assignments can also be employed on range images. A common solution is to select the range pixels inside 3D objects as positive samples, which has been adopted in [192, 69]. Different from other methods where the regression targets are based on the global 3D coordinate system, the range-based methods resort to an object-centric coordinate system for regression. Eqn. 14 can still be applied in these methods with an additional coordinate transform.

**Set-to-set assignment.** DETR [21] is an influential 2D detection method that introduces a set-to-set assignment strategy to automatically assign the predictions to the respective ground truths via the Hungarian algorithm [120]:

$$
\mathcal{M}^{*} = \underset {\mathcal{M}}{\operatorname{argmin}}\sum_{(i\rightarrow j)\in \mathcal{M}}L_{det}(b_{i}^{g},b_{j}), \quad (15)
$$

where \(\mathcal{M}\) is a one-to-one mapping from each positive sample to a 3D object. The set-to-set assignments have also been explored in 3D object detection approaches [196, 297, 332], and [332] further introduces a novel cost function for the Hungarian matching.

Table 7: A taxonomy of anchor-free detection methods based on the sample types for prediction and the assignment strategies.

| Method            | Samples for Prediction | Positive Samples Selection  |
| ----------------- | ---------------------- | --------------------------- |
| PIXOR [335]       | BEV grid cells         | inside objects              |
| CenterPoint [350] | BEV grid cells         | Gaussian radii on centers   |
| ObjectDGCNN [297] | BEV grid cells         | bipartite matching          |
| Pillar-OD [302]   | pillars                | inside objects              |
| HotSpotNet [36]   | voxels                 | K-nearest to object centers |
| PointRCNN [252]   | points                 | foreground                  |
| 3DSSD [342]       | points                 | foreground & near centers   |
| LaserNet [192]    | range pixels           | inside objects              |
| RangeDet [69]     | range pixels           | inside objects              |

**Analysis: potentials and challenges of the anchor-free approaches.** The anchor-free detection methods abandon the complicated anchor design and exhibit stronger flexibility in terms of the assignment strategies. With the anchor-free assignments, 3D objects can be predicted directly on various representations, including points, range pixels, voxels, pillars, and BEV grid cells. The learning process is also greatly simplified without introducing additional shape priors. Among those anchor-free methods, the center-based methods [350] have shown great potential in detecting small objects and have outperformed the anchor-based detection methods on the widely used benchmarks [15, 268].

Despite these merits, a general challenge to the anchor-free methods is to properly select positive samples to generate 3D object predictions. In contrast to the anchor-based methods that only select those high IoU samples, the anchor-free methods may possibly select some bad positive samples that yield inaccurate object predictions. Hence, careful design to filter out those bad positives is important in most anchor-free methods.

#### 3.2.3 3D object detection with auxiliary tasks

Numerous approaches resort to auxiliary tasks to enhance the spatial features and provide implicit guidance for accurate 3D object detection. The commonly used auxiliary tasks include semantic segmentation, intersection over union prediction, object shape completion, and object part estimation.

Table 8: A taxonomy of detection methods based on auxiliary tasks.

| Auxiliary Task          | Methods                            |
| ----------------------- | ---------------------------------- |
| Semantic segmentation   | [252, 340, 94, 379, 347, 339, 269] |
| IoU prediction          | [375, 376, 153, 81, 103]           |
| Object shape completion | [201, 388, 329, 328]               |
| Object part estimation  | [36, 254]                          |

**Semantic segmentation.** Semantic segmentation can help 3D object detection in 3 aspects: (1) Foreground segmentation could provide implicit information on objects' locations. Point-wise foreground segmentation has been broadly adopted in most point-based 3D object detectors [252, 379, 340, 94] for proposal generation. (2) Spatial features can be enhanced by segmentation. In [347], a semantic context encoder is leveraged to enhance spatial features with semantic knowledge. (3) Semantic segmentation can be utilized as a pre-processing step to filter out background samples and make 3D object detection more efficient. [339] and [269] leverage semantic segmentation to remove those redundant points to speed up the subsequent detection model.

**IoU prediction.** Intersection over union (IoU) can serve as a useful supervisory signal to rectify the object confidence scores. [375] proposes an auxiliary branch to predict an IoU score \(S*{IoU}\) for each detected 3D object. During inference, the original confidence scores \(S*{conf} = S*{cls}\) from the conventional classification branch are further rectified by the IoU scores \(S*{IoU}\) :

$$
S_{conf} = S_{cls}\cdot (S_{IoU})^{\beta}, \quad (16)
$$

where the hyper-parameter \(\beta\) controls the degrees of suppressing the low-IoU predictions and enhancing the high-IoU predictions. With the IoU rectification, the high-quality 3D objects are easier to be selected as the final predictions. Similar designs have also been adopted in [376, 153, 81, 103].

**Object shape completion.** Due to the nature of LiDAR sensors, faraway objects generally receive only a few points on their surfaces, so 3D objects are generally sparse and incomplete. A straightforward way of boosting the detection performance is to complete object shapes from sparse point clouds. Complete shapes could provide more useful information for accurate and robust detection. Many shape completion techniques have been proposed in 3D detection, including a shape decoder [201], shape signatures [388], and a probabilistic occupancy grid [329, 328].

**Object part estimation.** Identifying the part information inside objects is helpful in 3D object detection, as it reveals more fine-grained 3D structure information of an object. Object part estimation has been explored in some works [36, 254].

**Analysis: future prospects of multitask learning for 3D object detection.** 3D object detection is innately correlated with many other 3D perception and generation tasks. Multitask learning of 3D detection and segmentation is more beneficial compared to training 3D object detectors independently, and shape completion can also help 3D object detection. There are also other tasks that can help boost the performance of 3D object detectors. For instance, scene flow estimation could identify static and moving objects, and tracking the same 3D object in a point cloud sequence yields a more accurate estimation of this object. Hence, it will be promising to integrate more perception tasks into the existing 3D object detection pipeline.

Fig. 10: Chronological overview of the camera-based 3D object detection methods.

## 4 Camera-based 3D Object Detection

In this section, we introduce camera-based 3D object detection methods. In Section 4.1, we review and analyze the monocular 3D object detection methods, which can be further divided into the image-only, depth-assisted, and prior-guided approaches. In Section 4.2, we investigate the 3D object detection methods based on stereo images. In Section 4.3, we introduce the 3D object detection methods with multiple cameras. A chronological overview of the camera-based 3D object detection methods is shown in Figure 10.

### 4.1 Monocular 3D object detection

**Problem and Challenge.** Detecting objects in the 3D space from monocular images is an ill-posed problem since a single image cannot provide sufficient depth information. Accurately predicting the 3D locations of objects is the major challenge in monocular 3D object detection. Many endeavors have been made to tackle the object localization problem, e.g. inferring depth from images, leveraging geometric constraints and shape priors. Nevertheless, the problem is far from being solved. Monocular 3D detection methods still perform much worse than the LiDAR-based methods due the poor 3D localization ability, which leaves an open challenge to the research community.

#### 4.1.1 Image-only monocular 3D object detection

Inspired by the 2D detection approaches, a straightforward solution to monocular 3D object detection is to directly regress the 3D box parameters from images via a convolutional neural network. The direct-regression methods naturally borrow designs from the 2D detection network architectures, and can be trained in an end-to-end manner. These approaches can be divided into the single-stage/two-stage, or anchor-based/anchor-free methods. An illustration of image-only 3D object detection is shown in Figure 11 and a taxonomy is in Table 9.

**Single-stage anchor-based methods.** Anchor-based monocular detection approaches rely on a set of 2D-3D anchor boxes placed at each image pixel, and use a 2D convolutional neural network to regress object parameters from the anchors. Specifically, for each pixel \([u,v]\) on the image plane, a set of 3D anchors \([w^{a},h^{a},l^{a},\theta^{a}]_{3D}\) 2D anchors \([w^{a},h^{a}]_{2D}\) , and depth anchors \(d^{a}\) are pre-defined. An image is passed through a convolutional network to predict the 2D box offsets \(\delta*{2D} = [\delta*{x},\delta*{y},\delta*{w},\delta*{h}]*{2D}\) and the 3D box offsets \(\delta*{3D} = [\delta*{x},\delta*{y},\delta*{d},\delta*{w},\delta*{h},\delta*{l},\delta*{\theta}]_{3D}\) based on each anchor. Then, the 2D bounding boxes \(b_{2D} = [x,y,w,h]\_{2D}\) can be decoded as

$$
\begin{array}{rl} & {[x,y]_{2D} = [u,v] + [\delta_{x},\delta_{y}]_{2D}\cdot [w^{a},h^{a}]_{2D},}\\ & {[w,h]_{2D} = e^{[\delta_{w},\delta_{h}]_{2D}}\cdot [w^{a},h^{a}]_{2D},} \end{array} \quad (17)
$$

and the 3D bounding boxes \(b*{3D} = [x,y,z,l,w,h,\theta ]*{3D}\) can be decoded from the anchors and \(\delta\_{3D}\)

$$
\begin{array}{rl} & {[u^c,u^c] = [u,v] + [\delta_x,\delta_y]_{3D}\cdot [w^a,h^a]_{2D},}\\ & {[w,h,l]_{3D} = e^{[\delta_w,\delta_h,\delta_l]_{3D}}\cdot [w^a,h^a,l^a]_{3D},}\\ & {d^c = d^a +\delta_{d_{3D}},\theta_{3D} = \theta_{3D}^a +\delta_{\theta_{3D}},} \end{array} \quad (18)
$$

where \([u^{c},v^{c}]\) is the projected object center on the image plane. Finally, the projected center \([u^{c},v^{c}]\) and its depth \(d^{c}\) are transformed into the 3D object center \([x,y,z]\_{3D}\)

$$
d^{c}\cdot \left[ \begin{array}{c}u^{c}\\ v^{c}\\ 1 \end{array} \right] = K T\left[ \begin{array}{c}x\\ y\\ z\\ 1 \end{array} \right] \quad (19)
$$

where \(K\) and \(T\) are the camera intrinsics and extrinsics.

M3D-RPN [13] is a seminal paper that proposes the anchor-based framework, and many papers have tried to improve this framework, e.g. extending it into video-based 3D detection [14], introducing differential non-maximum suppression [121], designing an asymmetric attention module [173].

**Single-stage anchor-free methods.** Anchor-free monocular detection approaches predict the attributes of 3D objects from images without the aid of anchors. Specifically, an image is passed through a 2D convolutional neural network and then multiple heads are applied to predict the object attributes separately. The prediction heads generally include a category head to predict the object's category, a keypoint head to predict the coarse object center \([u,v]\) , an offset head to predict the center offset \([\delta_{x},\delta_{y}]\) based on \([u,v]\) , a depth head to predict the depth offset \(\delta\_{d}\) , a size head to predict the object size \([w,h,l]\) , and an orientation head to predict the observation angle \(\alpha\) . The 3D object center \([x,y,z]\) can be converted from the projected center \([u^{c},v^{c}]\) and depth \(d^{c}\) :

$$
d^c = \sigma^{-1}(\frac{1}{\delta_d + 1}),u^c = u + \delta_x,v^c = v + \delta_y,
$$

$$
d^c\cdot \left[ \begin{array}{c}u^c\\ v^c\\ 1 \end{array} \right] = K T\left[ \begin{array}{c}x\\ y\\ z\\ 1 \end{array} \right]_3D,
$$

where \(\sigma\) is the sigmoid function. The way angle \(\theta\) of an object can be converted from the observation angle \(\alpha\) using

$$
\theta = \alpha +\arctan (\frac{x}{z}). \quad (21)
$$

CenterNet [380] first introduces the single-stage anchor-free framework for monocular 3D object detection. Many following papers work on improving this framework, including novel depth estimation schemes [166, 294, 369], an FCOS [275]-like architecture [293], a new IoU-based loss function [178], keypoints [135], pair-wise relationships [47], camera extrinsics prediction [384], and view transforms [241, 237, 262].

Fig. 11: An illustration of image-only monocular 3D object detection methods. Image samples are from [293].

**Two-stage methods.** Two-stage monocular detection approaches generally extend the conventional two-stage 2D detection architectures to 3D object detection. Specifically, they utilize a 2D detector in the first stage to generate 2D bounding boxes from an input image. Then in the second stage, the 2D boxes are lifted up to the 3D space by predicting the 3D object parameters from the 2D RoIs. ROI-10D [182] extends the conventional Faster RCNN [239] architecture with a novel head to predict the parameters of 3D objects in the second stage. A similar design paradigm has been adopted in many works with improvements like disentangling the 2D and 3D detection loss [261], predicting heading angles in the first stage [127], learning more accurate depth information [233, 258, 172].

Table 9: A taxonomy of image-only monocular detection methods based on frameworks.

| Framework                 | Methods                                                       |
| ------------------------- | ------------------------------------------------------------- |
| Single-stage anchor-based | [13, 14, 121, 173, 159]                                       |
| Single-stage anchor-free  | [380, 197, 166, 293, 294, 178] [135, 369, 384, 241, 237, 262] |
| Two-stage                 | [182, 261, 127, 233, 258, 172]                                |

**Analysis: potentials and challenges of the image-only methods.** The image-only methods aim to directly regress the 3D box parameters from images via a modified 2D object detection framework. Since these methods take inspiration from the 2D detection methods, they can naturally benefit from the advances in 2D object detection and image-based network architectures. Most methods can be trained end-to-end without pre-training or post-processing, which is quite simple and efficient.

A critical challenge of the image-only methods is to accurately predict depth \(d^c\) for each 3D object. As shown in [294], simply replacing the predicted depth with ground truth yields more than \(20\%\) car AP gain on the KITTI [82] dataset, while replacing other parameters only results in an incremental gain. This observation indicates that the depth error dominates the total errors and becomes the most critical factor hampering accurate monocular detection. Nevertheless, depth estimation from monocular images is an ill-posed problem, and the problem becomes severer with only box-level supervisory signals.

#### 4.1.2 Depth-assisted monocular 3D object detection

Depth estimation is critical in monocular 3D object detection. To achieve more accurate monocular detection results, many papers resort to pre-training an auxiliary depth estimation network. Specifically, a monocular image is first passed through a pretrained depth estimator, e.g. MonoDepth [85] or DORN [78], to generate a depth image. Then, there are mainly two categories of methods to deal with depth images and monocular images. The depth-image based methods fuse images and depth maps with a specialized neural network to generate depth-aware features that could enhance the detection performance. The pseudo-LiDAR based methods convert a depth image into a pseudo-LiDAR point cloud, and LiDAR-based detectors can then be applied to the point cloud to predict 3D objects. An illustration of depth-assisted monocular 3D object detection is shown in Figure 12 and a taxonomy of these methods is in Table 10.

Table 10: A taxonomy of depth-assisted monocular detection methods based on data representations and detection networks (2D: convolutional networks; 3D: point cloud networks).

| Method             | RGB | Depth | Pseudo LiDAR | Coord. Map | 2D  | 3D  |
| ------------------ | --- | ----- | ------------ | ---------- | --- | --- |
| MultiFusion [326]  | ✓   | ✓     |              |            | ✓   |     |
| D4LCN [60]         | ✓   | ✓     |              |            | ✓   |     |
| DDMP [288]         | ✓   | ✓     |              |            | ✓   |     |
| Pseudo-LiDAR [298] |     |       | ✓            |            |     | ✓   |
| Deep Optics [28]   |     |       | ✓            |            |     | ✓   |
| AM3D [176]         | ✓   |       | ✓            |            | ✓   | ✓   |
| Weng et al. [312]  | ✓   |       | ✓            |            | ✓   | ✓   |
| PatchNet[177]      |     |       |              | ✓          | ✓   |     |

**Depth-image based methods.** Most depth-image based methods leverage two backbone networks for RGB and depth images respectively. They obtain depth-aware image features by fusing the information from the two backbones with specialized operators. More accurate 3D bounding boxes can be learned from the depth-aware features and can be further refined with depth images. MultiFusion [326] is a pioneering work that introduces the depth-image based detection framework. Following papers adopt similar design paradigms with improvements in network architectures, operators, and training strategies, e.g. a point-based attentional network [7], depth-guided convolutions [60], depth conditioned message passing [288], disentangling appearance and localization features [390], and a novel depth pre-training framework [211].

Fig. 12: An illustration of depth-assisted monocular 3D object detection methods. Image and depth samples are from [176].

**Pseudo-LiDAR based methods.** Pseudo-LiDAR based methods transform a depth image into a pseudo-LiDAR point cloud, and LiDAR-based detectors can then be employed to detect 3D objects from the point cloud. Pseudo-LiDAR point cloud is a data representation first introduced in [298], where they convert a depth map \(\mathcal{D} \in R^{H \times W}\) into a pseudo point cloud \(\mathcal{P} \in R^{HW \times 3}\) . Specifically, for each pixel \([u, v]\) and its depth value \(d\) in a depth image, the corresponding 3D point coordinate \([x, y, z]\) in the camera coordinate system is computed as

$$
x = \frac{(u - c_u)\times z}{f_u},y = \frac{(v - c_v)\times z}{f_v},z = d, \quad (22)
$$

where \([c_u, c_v]\) is the camera principal point, and \(f_u\) and \(f_v\) are the focal lengths along the horizontal and vertical axis respectively. Thus \(\mathcal{P}\) can be obtained by back-projecting each pixel in \(\mathcal{D}\) into the 3D space. \(\mathcal{P}\) is referred as the pseudo-LiDAR representation: it is essentially a 3D point cloud but is extracted from a depth image instead of a real LiDAR sensor. Finally, LiDAR-based 3D object detectors can be directly applied on the pseudo-LiDAR point cloud \(\mathcal{P}\) to predict 3D objects. Many papers have worked on improving the pseudo-LiDAR detection framework, including augmenting pseudo point cloud with color information [176], introducing instance segmentation [312], designing a progressive coordinate transform scheme [289], improving pixel-wise depth estimation with separate foreground and background prediction [296], domain adaptation from real LiDAR point cloud [345], and a new physical sensor design [28].

PatchNet [177] challenges the conventional idea of leveraging the pseudo-LiDAR representation \(\mathcal{P} \in R^{HW \times 3}\) for monocular 3D object detection. They conduct an in-depth investigation and provide an insightful observation that the power of pseudo-LiDAR representation comes from the coordinate transformation instead of the point cloud representation. Hence, a coordinate map \(\mathcal{M} \in R^{H \times W \times 3}\) where each pixel encodes a 3D coordinate can attain a comparable monocular detection result with the pseudo-LiDAR point cloud representation. This observation enables us to directly apply a 2D neural network on the coordinate map to predict 3D objects, eliminating the need of leveraging the time-consuming LiDAR-based detectors on point clouds.

**Analysis: potentials and challenges of the depth-assisted approaches.** The depth-assisted approaches pursue more accurate depth estimation by leveraging a pre-trained depth prediction network. Both the depth image representation and the pseudo-LiDAR presentation could significantly boost the monocular detection performance. Nevertheless, compared to the image-only methods that only require 3D box annotations, pre-training a depth prediction network requires expensive ground truth depth maps, and it also hampers the end-to-end training of the whole framework. Furthermore, pre-trained depth estimation networks suffer from poor generalization ability. Pretrained depth maps are usually not well calibrated on the target dataset and typically the scale needs to be adapted to the target dataset. Thus there remains a non-negligible domain gap between the source domain leveraged for depth pre-training and the target domain for monocular detection. Given the fact that driving scenarios are normally diverse and complex, pre-training depth networks on a restricted domain may not work well in real-world applications.

#### 4.1.3 Prior-guided monocular 3D object detection

Numerous approaches try to tackle the ill-posed monocular 3D object detection problem by leveraging the hidden prior knowledge of object shapes and scene geometry from images. The prior knowledge can be learned by introducing pre-trained subnetworks or auxiliary tasks, and they can provide extra information or constraints to help accurately localize 3D objects. The broadly adopted prior knowledge includes object shapes, geometry consistency, temporal constraints, and segmentation information. An illustration of the prior types is shown in Figure 13.

Fig. 13: An illustration of the prior types in monocular 3D object detection methods. Samples are from [39, 98, 319, 9, 213].

**Object shapes.** Many methods resort to shape reconstruction of 3D objects directly from images. The reconstructed shapes can be further leveraged to determine the locations and poses of the 3D objects. There are 5 types of reconstructed representations: computer-aided design (CAD) models, wireframe models, signed distance function (SDF), points, and voxels.

Some papers [362, 25, 98] learn morphable wireframe models to represent 3D objects. Other works [122, 182, 359, 9] leverage DeepSDF [213] to learn implicit signed distance functions or low-dimensional shape parameters from CAD models, and they further propose a render-and-compare approach to learn the parameters of 3D objects. Some works [319, 320] utilize voxel patterns to represent 3D objects. Other papers [118, 31] resort to point cloud reconstruction from images and estimate the locations of 3D objects with 2D-3D correspondences.

**Geometric consistency.** Given the extrinsics matrix \(T \in SE(3)\) that transforms a 3D coordinate in the object frame to the camera frame, and the camera intrinsics matrix \(K\) that project the 3D coordinate onto the image plane, the projection of a 3D point \([x, y, z]\) in the object frame into the image pixel coordinate \([u, v]\) can be represented as

$$
d\cdot \left[ \begin{array}{c}u\\ v\\ 1 \end{array} \right] = K T\left[ \begin{array}{c}x\\ y\\ z\\ 1 \end{array} \right], \quad (23)
$$

where \(d\) is the depth of transformed 3D coordinate in the camera frame. Eqn. 23 provides a geometric relationship between 3D points and 2D image pixel coordinates, which can be leveraged in various ways to encourage consistency between the predicted 3D objects and the 2D objects on images. There are mainly 5 types of geometric constraints in monocular detection: 2D-3D boxes consistency, keypoints, object's height-depth relationship, inter-objects relationship, and ground plane constraints.

Some works [197, 13, 112, 200] propose to encourage the consistency between 2D and 3D boxes by minimizing reprojection errors. These methods introduce a post-processing step to optimize the 3D object parameters by gradually fitting the projected 3D boxes to 2D bounding boxes on images. There is also a branch of papers [135, 257, 133] that predict the object keypoints from images, and the keypoints can be leveraged to calibrate the sizes of locations of 3D objects. Object's height-depth relationship can also serve as a strong geometric prior. Specifically, given the physical height of an object \(H\) in the 3D space, the visual height \(h\) on images, and the corresponding depth of the object \(d\) , there exists a geometric constraint: \(d = f \cdot H / h\) , where \(f\) is the camera focal length. This constraint can be leveraged to obtain more accurate depth estimation and has been broadly applied in a lot of works [17, 369, 172, 258]. There are also some papers [381, 47] trying to model the inter-objects relationships by exploiting new geometric relations among objects. Other papers [39, 13, 159, 161] leverage the assumption that 3D objects are generally on the ground plane to better localize those objects.

**Temporal constraints.** Temporal association of 3D objects can be leveraged as strong prior knowledge. The temporal object relationships have been exploited as depth-ordering [100] and multi-frame object fusion with a 3D Kalman filter [14].

Table 11: A taxonomy of prior-guided monocular detection methods based on prior types.

| Prior Types           | Methods                          |
| --------------------- | -------------------------------- |
| Object shape          | wireframe [362, 25, 98]          |
|                       | SDF [122, 182, 9, 359]           |
|                       | points [31, 118]                 |
|                       | voxels [319, 320]                |
| Geometric consistency | 2D-3D boxes [197, 13, 112, 200]  |
|                       | keypoints [135, 133, 257]        |
|                       | height-depth [17, 172, 369, 258] |
|                       | inter-objects [381, 47]          |
|                       | ground plane [39, 161, 13, 159]  |
| Temporal constraints  | [100, 14]                        |
| Segmentation          | [319, 9, 39, 99]                 |

**Segmentation** Image segmentation helps monocular 3D object detection mainly in two aspects. First, object segmentation masks are crucial for instance shape reconstruction in some works [319, 9]. Second, segmentation indicates whether an image pixel is inside a 3D object from the perspective view, and this information has been utilized in [39, 99] to help localize 3D objects.

**Analysis: potentials and challenges of leveraging prior knowledge in monocular 3D detection.** With shape reconstruction, we could obtain more detailed object shape information from images, which is beneficial to 3D object detection. We can also attain more accurate detection results through the projection or render-and-compare loss. However, there exist two challenges for shape reconstruction applied in monocular 3D object detection. First, shape reconstruction normally requires an additional step of pre-training a reconstruction network, which hampers end-to-end training of the monocular detection pipeline. Second, object shapes are generally learned from CAD models instead of real-world instances, which imposes the challenge of generalizing the reconstructed objects to real-world scenarios.

Geometric consistencies are broadly adopted and can help improve detection accuracy. Nevertheless, some methods formulate the geometric consistency as an optimization problem and optimize object parameters in post-processing, which is quite time-consuming and hampers end-to-end training.

Image segmentation is useful information in monocular 3D detection. However, training segmentation networks requires expensive pixel annotations. Pre-training segmentation models on external datasets will suffer from the generalization problem.

### 4.2 Stereo-based 3D object detection

**Problem and Challenge.** Stereo-based 3D object detection aims to detect 3D objects from a pair of images. Compared to monocular images, paired stereo images provide additional geometric constraints that can be utilized to infer more accurate depth information. Hence, the stereo-based methods generally obtain a better detection performance than the monocular-based methods. Nevertheless, stereo cameras typically require very accurate calibration and synchronization, which are normally difficult to achieve in real applications. An illustration of stereo-based 3D object detection approaches is shown in Figure 14 and a taxonomy is in Table 12.

Fig. 14: An illustration of stereo-based 3D object detection methods. Image and disparity samples are from [231].

**Stereo matching and depth estimation.** A stereo camera can produce a pair of images, i.e. the left image \(\mathcal{I}\_L\) and the right image \(\mathcal{I}\_R\) in one shot. With the stereo matching techniques [188, 29], a disparity map can be estimated from the paired stereo images leveraging multi-view geometry [93]. Ideally, for each pixel on the left image \(\mathcal{I}\_L(u,v)\) , there exists a pixel on the right image \(\mathcal{I}\_R(u,v + p)\) with the disparity value \(p\) so that the two pixels picture the same 3D location. Finally, the disparity map can be transformed into a depth image with the following formula:

$$
d = \frac{f\times b}{p}, \quad (24)
$$

where \(d\) is the depth value, \(f\) is the focal length, and \(b\) is the baseline length of the stereo camera. The pixel-wise disparity constraints from stereo images enable more accurate depth estimation compared to monocular depth prediction.

**2D-detection based methods.** Conventional 2D object detection frameworks can be modified to resolve the stereo detection problem. Specifically, paired stereo images are passed through an image-based detector with Siamese backbone networks to generate left and right regions of interest (RoIs) for the left and right images respectively. Then in the second stage, the left and right RoIs are fused to estimate the parameters of 3D objects. Stereo R-CNN [134] first proposes to extend 2D detection frameworks to stereo 3D detection. This design paradigm has been adopted in numerous papers. [234] proposes a novel stereo triangulation learning sub-network at the second stage; [331, 223, 267, 32] learn instance-level disparity by object-centric stereo matching and instance segmentation; [216] proposes adaptive instance disparity estimation; [160, 217] introduce single-stage stereo detection frameworks; [38, 40] propose an energy-based framework for stereo-based 3D object detection.

Table 12: A taxonomy of stereo-based detection methods based on auxiliary tasks and data representations.

| Method              | 2D Det. | 2D Seg. | Disp./Depth | Pseudo LiDAR | 3D Volume |
| ------------------- | ------- | ------- | ----------- | ------------ | --------- |
| 3DOP [38]           |         |         | ✓           |              |           |
| TLNet [234]         | ✓       |         |             |              |           |
| Stereo R-CNN [134]  | ✓       |         |             |              |           |
| Disp R-CNN [267]    | ✓       | ✓       | ✓           |              |           |
| ZoomNet [331]       | ✓       | ✓       | ✓           |              |           |
| OC-Stereo [223]     | ✓       | ✓       | ✓           |              |           |
| IDA-3D [216]        | ✓       |         | ✓           |              |           |
| YOLO-Stereo3D [160] |         |         | ✓           |              |           |
| SIDE [217]          | ✓       |         | ✓           |              |           |
| P-LiDAR++ [354]     |         |         | ✓           | ✓            |           |
| Qian et al. [231]   |         |         | ✓           | ✓            |           |
| CDN [80]            |         |         | ✓           | ✓            |           |
| RT3D-Stereo [116]   |         | ✓       | ✓           | ✓            |           |
| CG-Stereo [128]     |         | ✓       | ✓           | ✓            |           |
| LIGA-Stereo [89]    |         | ✓       | ✓           |              |           |
| DSGN [46]           |         |         | ✓           |              | ✓         |
| PLUMENet [304]      |         |         | ✓           |              | ✓         |

**Pseudo-LiDAR based methods.** The disparity map predicted from stereo images can be transformed into the depth image and then converted into the pseudo-LiDAR point cloud. Hence, similar to the monocular detection methods, the pseudo-LiDAR representation can also be employed in stereo-based 3D object detection methods. Those methods try to improve the disparity estimation in stereo matching for more accurate depth prediction. [354] introduces a depth cost volume in stereo matching networks; [231] proposes an end-to-end stereo matching and detection framework; [116, 128] leverage semantic segmentation and predict disparity for foreground and background regions separately; [80] proposes a Wasserstein loss for disparity estimation.

**Volume-based methods.** There exists a category of methods that skip the pseudo-LiDAR representation and perform 3D object detection directly on 3D stereo volumes. DSGN [46] proposes a 3D geometric volume derived from stereo matching networks and applies a grid-based 3D detector on the volume to detect 3D objects. [89] and [304] improve [46] by leveraging knowledge distillation and 3D feature volumes respectively.

**Potentials and challenges of the stereo-based methods.** Compared to the monocular detection methods, the stereo-based methods can obtain more accurate depth and disparity estimation with stereo matching techniques, which brings a stronger object localization ability and significantly boosts the 3D object detection performance. Nevertheless, an auxiliary stereo matching network brings additional time and memory consumption. Compared to LiDAR-based 3D object detection, detection from stereo images can serve as a much cheaper solution for 3D perception in autonomous driving scenarios. However, there still exists a nonnegligible performance gap between the stereo-based and the LiDAR-based 3D object detection approaches.

### 4.3 Multi-view 3D object detection

**Problem and Challenge.** Autonomous vehicles are generally equipped with multiple cameras to obtain complete environmental information from multiple viewpoints. Recently, multi-view 3D object detection has evolved rapidly. Some multi-view 3D detection approaches try to construct a unified BEV space by projecting multi-view images into the bird's-eye view, and then employ a BEV-based detector on top of the unified BEV feature map to detect 3D objects. The transformation from camera views to the bird's-eye view is ambiguous without accurate depth information, so image pixels and their BEV locations are not perfectly aligned. How to build reliable transformations from camera views to the bird's-eye view is a major challenge in these methods. Other methods resort to 3D object queries that are generated from the bird's-eye view and Transformers where cross-view attention is applied to object queries and multi-view image features. The major challenge is how to properly generate 3D object queries and design more effective attention mechanisms in Transformers.

**BEV-based multi-view 3D object detection.** LSS [219] is a pioneering work that proposes a lift-splat-shoot paradigm to solve the problem of BEV perception from multi-view cameras. There are three steps in LSS. Lift: bin-based depth prediction is conducted on image pixels and multi-view image features are lifted to 3D frustums with depth bins. Splat: 3D frustums are splatted into a unified bird's-eye view plane and image features are transformed into BEV features in an end-to-end manner. Shoot: downstream perception tasks are performed on top of the BEV feature map. This paradigm has been successfully adopted by many following works. BEVDet [106, 105] improves LSS [219] with a four-step multi-view detection pipeline, where the image view encoder encodes features from multi-view images, the view transformer transforms image features from camera views to the bird's-eye view, the BEV encoder further encodes the BEV features, and the detection head is employed on top of the BEV features for 3D detection. The major bottleneck in [106, 219] is depth prediction, as it is normally inaccurate and will result in inaccurate feature transforms from camera views to the bird's-eye view. To obtain more accurate depth information, many papers resort to mining additional information from multi-view images and past frames, e.g. [140] leverages explicit depth supervision, [309] introduces surround-view temporal stereo, [138] uses dynamic temporal stereo, [212] combines both short-term and long-term temporal stereo for depth prediction. In addition, there are also some papers [323, 104] that completely abandon the design of depth bins and categorical depth prediction. They simply assume that the depth distribution along the ray is uniform, so the camera-to-BEV transformation can be conducted with higher efficiency.

**Query-based multi-view 3D object detection.** In addition to the BEV-based approaches, there is also a category of methods where object queries are generated from the bird's-eye view and interact with camera view features. Inspired by the advances in Transformers for object detection [21], DETR3D [305] introduces a sparse set of 3D object queries, and each query corresponds to a 3D reference point. The 3D reference points can collect image features by projecting their 3D locations onto the multi-view image planes and then object queries interact with image features through Transformer layers. Finally, each object query will decode a 3D bounding box. Many following papers try to improve this design paradigm, such as introducing spatiallyaware cross-view attention [61] and adding 3D positional embeddings on top of image features [162]. BEVFormer [145] introduces dense grid-based BEV queries and each query corresponds to a pillar that contains a set of 3D reference points. Spatial cross-attention is applied to object queries and sparse image features to obtain spatial information, and temporal selfattention is applied to object queries and past BEV queries to fuse temporal information.

Fig. 15: An illustration of multi-view 3D object detection methods. Figures are from [219] and [305].

## 5 Multi-Modal 3D Object Detection

In this section, we introduce the multi-modal 3D object detection approaches that fuse multiple sensory inputs. According to the sensor types, the approaches can be divided into three categories: LiDAR-camera, radar, and map fusion-based methods. In Section 5.1, we review and analyze the multi-modal detection approaches with LiDAR-camera fusion, including the early-fusion based, the intermediate-fusion based, and the late-fusion basedmethods. In Section 5.2, we investigate the multi-modal detection approaches with radar signals. In Section 5.3, we introducethe multi-modal 3D detection approaches with high-definition maps. A chronological overview of the multi-modal 3D object detection approaches is shown in Figure 16.

Table 13: A taxonomy of multi-sensor fusion-based detection methods based on fused stages, representations, and operators.

| Method              | Input | Backbone | Proposal | RoI | Output | Camera rep.      | LiDAR rep.          | Fusion Operator        |
| ------------------- | ----- | -------- | -------- | --- | ------ | ---------------- | ------------------- | ---------------------- |
| F-PointNet [226]    | ✓     |          |          |     |        | frustum          | point cloud         | region selection       |
| F-ConvNet [306]     | ✓     |          |          |     |        | frustum          | point cloud         | region selection       |
| RoarNet [259]       | ✓     |          |          |     |        | 2D boxes & poses | point cloud         | region selection       |
| PointPainting [281] | ✓     |          |          |     |        | 2D segmentation  | point cloud         | point-wise append      |
| MVX-Net [264]       |       | ✓        |          |     |        | image features   | voxels              | concatenation & MLP    |
| ContFuse [147]      |       | ✓        |          |     |        | image features   | BEV features        | continuous convolution |
| PointFusion [327]   |       | ✓        |          |     |        | image features   | point features      | concatenation & MLP    |
| EPNet [109]         |       | ✓        |          |     |        | image features   | point features      | point-wise attention   |
| MMF [148]           |       | ✓        | ✓        | ✓   |        | image features   | BEV features        | continuous convolution |
| 3D-CVF [353]        |       | ✓        | ✓        | ✓   |        | image features   | BEV features        | gated attention        |
| MV3D [41]           |       |          | ✓        | ✓   |        | image features   | multi-view features | concatenation & MLP    |
| AVOD [117]          |       |          | ✓        | ✓   |        | image features   | BEV features        | concatenation & MLP    |
| CLOCs [209]         |       |          |          |     | ✓      | 2D boxes         | 3D boxes            | box consistency        |

Fig. 16: Chronological overview of the multi-modal 3D object detection methods.

### 5.1 Multi-modal detection with LiDAR-camera fusion

**Problem and Challenge.** Camera and LiDAR are two complementary sensor types for 3D object detection. Cameras provide color information from which rich semantic features can be extracted, while LiDAR sensors specialize in 3D localization and provide rich information about 3D structures. Many endeavors have been made to fuse the information from cameras and LiDARs for accurate 3D object detection. Since LiDAR-based detection methods perform much better than camera-based methods, the state-of-the-art approaches are mainly based on LiDAR-based 3D object detectors and try to incorporate image information into different stages of a LiDAR detection pipeline. In view of the complexity of LiDAR-based and camera-based detection systems, combining the two modalities together inevitably brings additional computational overhead and inference time latency. Therefore, how to efficiently fuse the multi-modal information remains an open challenge. A taxonomy of multi-modal 3D object detection methods is in Table 13.

### 5.1.1 Early-fusion based 3D object detection

Early-fusion based methods aim to incorporate the knowledge from images into point cloud before they are fed into a LiDAR based detection pipeline. Hence the early-fusion frameworks are generally built in a sequential manner: 2D detection or segmentation networks are firstly employed to extract knowledge from images, and then the image knowledge is passed to point cloud, and finally the enhanced point cloud is fed to a LiDAR-based 3D object detector. Based on the fusion types, the early-fusion methods can be divided into two categories: region-level knowledge fusion and point-level knowledge fusion. An illustration of the early-fusion based approaches is shown in Figure 17.

**Region-level knowledge fusion.** Region-level fusion methods aim to leverage knowledge from images to narrow down the object candidate regions in 3D point cloud. Specifically, an image is first passed through a 2D object detector to generate 2D bounding boxes, and then the 2D boxes are extruded into 3D viewing frustums. The 3D viewing frustums are applied on LiDAR point cloud to reduce the searching space. Finally, only the selected point cloud regions are fed into a LiDAR detector for 3D object detection. F-PointNet [226] first proposes this fusion mechanism, and many endeavors have been made to improve the fusion framework. [306] divides a viewing frustum into grid cells and applies a convolutional network on the grid cells for 3D detection; [259] proposes a novel geometric agreement search; [206] exploits the pillar representation; [67] introduces a model fitting algorithm to find the object point cloud inside each frustum.

**Point-level knowledge fusion.** Point-level fusion methods aim to augment input point cloud with image features. The augmented point cloud is then fed into a LiDAR detector to attain a better detection result. PointPainting [281] is a seminal work that leverages image-based semantic segmentation to augment point clouds. Specifically, an image is passed through a segmentation network to obtain pixel-wise semantic labels, and then the semantic labels are attached to the 3D points by point-to-pixel projection. Finally, the points with semantic labels are fed into a LiDAR-based 3D object detector. This design paradigm has been followed by a lot of papers [330, 260, 191]. Apart from semantic segmentation, there also exist some works trying to exploit other information from images, e.g. depth image completion [351].

**Analysis: potentials and challenges of the early-fusion methods.** The early-fusion based methods focus on augmenting point clouds with image information before they are passed through a LiDAR 3D object detection pipeline. Most methods are compatible with a wide range of LiDAR-based 3D object detectors and can serve as a quite effective pre-processing step to boost detection performance. Nevertheless, the early-fusion methods generally perform multi-modal fusion and 3D object detection in a sequential manner, which brings additional inference latency. Given the fact that the fusion step generally requires a complicated 2D object detection or semantic segmentation network, the time cost brought by multi-modal fusion is normally non-negligible. Hence, how to perform multi-modal fusion efficiently at the early stage has become a critical challenge.

Fig. 17: An illustration of early-fusion based 3D object detection methods.

Fig. 18: An illustration of intermediate-fusion based 3D object detection methods.

followed by a lot of papers [330, 260, 191]. Apart from semantic segmentation, there also exist some works trying to exploit other information from images, e.g. depth image completion [351].

**Analysis: potentials and challenges of the early-fusion methods.** The early-fusion based methods focus on augmenting point clouds with image information before they are passed through a LiDAR 3D object detection pipeline. Most methods are compatible with a wide range of LiDAR-based 3D object detectors and can serve as a quite effective pre-processing step to boost detection performance. Nevertheless, the early-fusion methods generally perform multi-modal fusion and 3D object detection in a sequential manner, which brings additional inference latency. Given the fact that the fusion step generally requires a complicated 2D object detection or semantic segmentation network, the time cost brought by multi-modal fusion is normally non-negligible. Hence, how to perform multi-modal fusion efficiently at the early stage has become a critical challenge.

#### 5.1.2 Intermediate-fusion based 3D object detection

Intermediate-fusion based methods try to fuse image and LiDAR features at the intermediate stages of a LiDAR-based 3D object detector, e.g. in backbone networks, at the proposal generation stage, or at the RoI refinement stage. These methods can also be classified according to the fusion stages. An illustration of intermediate-fusion based approaches is shown in Figure 18.

**Fusion in backbone networks.** Many endeavors have been made to progressively fuse image and LiDAR features in the backbone networks. In those methods, point-to-pixel correspondences are firstly established by LiDAR-to-camera transform, and then with the point-to-pixel correspondences, features from a LiDAR backbone can be fused with features from an image backbone through different fusion operators. The multi-modal fusion can be conducted in the intermediate layers of a grid-based detection backbone, with novel fusion operators such as continuous convolutions [291, 147, 148], hybrid voxel feature encoding [264], and Transformer [142, 370]. The multi-modal fusion can also be conducted only at the output feature maps of backbone networks, with fusion modules and operators including gated attention [353], unified object queries [43], BEV pooling [170], learnable alignments [50], point-to-ray fusion [141], Transformer [6], and other techniques [64, 45, 282]. In addition to the fusion in grid-based backbones, there also exist some papers incorporating image information into the point-based detection backbones [327, 109, 324, 308, 387].

**Fusion in proposal generation and RoI head.** There exists a category of works that conduct multi-modal feature fusion at the proposal generation and RoI refinement stage. In those methods, 3D object proposals are first generated from a LiDAR detector, and then the 3D proposals are projected into multiple views, i.e. the image view and bird's-eye view, to crop features from the image and LiDAR backbone respectively. Finally, the cropped image and LiDAR features are fused in an RoI head to predict parameters for each 3D object. MV3D [41] and AVOD [117] are pioneering works leveraging multi-view aggregation for multimodal detection. Other papers [43, 6] use the Transformer [280] decoder as the RoI head for multi-modal feature fusion.

**Analysis: potentials and challenges of the intermediate-fusion methods.** The intermediate methods encourage deeper integration of multi-modal representations and yield 3D boxes of higher quality. Nevertheless, camera and LiDAR features are intrinsically heterogeneous and come from different viewpoints, so there still exist some problems on the fusion mechanisms and view alignments. Hence, how to fuse the heterogeneous data effectively and how to deal with the feature aggregation from multiple views remain a challenge to the research community.

#### 5.1.3 Late-fusion based 3D object detection

**Fusion at the box level.** Late-fusion based approaches operate on the outputs, i.e. 3D and 2D bounding boxes, from a LiDAR-based 3D object detector and an image-based 2D object detector respectively. An illustration of late-fusion based approaches is shown in Figure 19. In those methods, object detection with camera and LiDAR sensor can be conducted in parallel, and the output 2D and 3D boxes are fused to yield more accurate 3D detection results. CLOCs [209] introduces a sparse tensor that contains paired 2D-3D boxes and learns the final object confidence scores from this sparse tensor. [210] improves [209] by introducing a light-weight 3D detector-cued image detector.

Fig. 19: An illustration of late-fusion based 3D object detection methods.

**Analysis: potentials and challenges of the late-fusion methods.** The late-fusion based approaches focus on the instancelevel aggregation and perform multi-modal fusion only on the outputs of different modalities, which avoids complicated interactions on the intermediate features or on the input point cloud. Hence these methods are much more efficient compared to other approaches. However, without resorting to deep features from camera and LiDAR sensors, these methods fail to integrate rich semantic information of different modalities, which limits the potential of this category of methods.

### 5.2 Multi-modal detection with radar signals

**Problem and Challenge.** Radar is an important sensory type in driving systems. In contrast to LiDAR sensors, radar has four irreplaceable advantages in real-world applications: Radar is much cheaper than LiDAR sensors; Radar is less vulnerable to extreme weather conditions; Radar has a larger detection range; Radar provides additional velocity measurements. Nevertheless, compared to LiDAR sensors that generate dense point clouds, radar only provides sparse and noisy measurements. Hence, how to effectively handle the radar signals remains a critical challenge.

**Radar-LiDAR fusion.** Many papers try to fuse the two modalities by introducing new fusion mechanisms to enable message passing between the radar and LiDAR signals, including voxel-based fusion [336], attention-based fusion [230], introducing a range-azimuth-doppler tensor [181], leveraging graph neural networks [194], exploiting dynamic occupancy maps [287], and introducing 4D radar data [207].

**Radar-camera fusion.** Radar-camera fusion is quite similar to LiDAR-camera fusion, as both radar and LiDAR data are 3D point representations. Most radar-camera approaches [26, 198, 199] adapt the existing LiDAR-based detection architectures to handle sparse radar points and adopt similar fusion strategies as LiDAR-camera based methods.

### 5.3 Multi-modal detection with high-definition maps

**Problem and Challenge.** High-definition maps (HD maps) contain detailed road information such as road shape, road marking, traffic signs, barriers, etc. HD maps provide rich semantic information on surrounding environments and can be leveraged as a strong prior to assist 3D object detection. How to effectively incorporate map information into a 3D object detection framework has become an open challenge to the research community.

**Multi-modal detection with map information.** High-definition maps can be readily transformed into a bird's-eye view representation and fused with rasterized BEV point clouds or feature maps. The fusion can be conducted by simply concatenating the channels of a rasterized point cloud and an HD map from the bird's-eye view [334], feeding LiDAR point cloud and HD map into separate backbones and fusing the output feature maps of the two modalities [72], or simply filtering out those predictions that do not fall into the relevant map regions [15]. Other map types have also been explored, e.g. visibility map [102], vectorized map [111].

## 6 Transformer-based 3D Object Detection

In this section, we introduce the Transformer-based 3D object detection methods. Transformers [280] have shown prominent performance in many computer vision tasks, and many endeavors have been made to adapt Transformers to 3D object detection. In Section 6.1, we review the Transformers tailored for 3D object detection from an architectural perspective. In Section 6.2, we introduce the applications of Transformers in different 3D object detectors.

Fig. 20: Chronological overview of Transformer-based 3D object detectors.

### 6.1 Transformer architectures for 3D object detection

**Problem and Challenge.** While most 3D object detectors are based on convolutional architectures, recently Transformer-based 3D detectors have shown great potential and dominated 3D object detection leaderboards. Compared to convolutional networks, the query-key-value design in Transformers enables more flexible interactions between different representations and the self-attention mechanism results in a larger receptive field than convolutions. However, fully-connected self-attention has quadratic time and space complexity w.r.t. the number of inputs, training Transformers can easily fall into sub-optimal results when the data size is small. Hence, it's critical to define proper query-key-value triplets and design specialized attention mechanisms for Transformer-based 3D object detectors.

**Transformer architectures.** The development of Transformer architectures in 3D object detection has experienced three stages: (1) Inspired by vanilla Transformer [280], new Transformer modules with special attention mechanisms are proposed to obtain more powerful features in 3D object detection. (2) Inspired by DETR [21], query-based Transformer encoder-decoder designs are introduced to 3D object detectors. (3) Inspired by ViT [63], patch-based inputs and architectures similar to Vision Transformers are introduced in 3D object detection.

In the first stage, many papers try to introduce novel Transformer modules into conventional 3D detection pipelines. In these papers, the choices of query, key, and value are quite flexible and new attention mechanisms are proposed. Pointformer [208] introduces Transformer modules to point backbones. It takes point features and coordinates as queries and applies self-attention to a group of point clouds. Voxel Transformer [187] replaces convolutional voxel backbones with Transformer modules, where sparse and submanifold voxel attention are proposed and applied to voxels. CT3D [250] proposes a novel Transformer-based detection head, where proposal-to-point attention and channel-wise attention are introduced.

In the second stage, many papers propose DETR-like architectures for 3D object detection. They leverage a set of object queries and use those queries to interact with different features to predict 3D boxes. DETR3D [305] introduces object queries and generates a 3D reference point for each query. They use reference points to aggregate multi-view image features as keys and values, and apply cross-attention between object queries and image features. Finally, each query can decode a 3D bounding box for detection. Many following works have adopted the design of object queries and reference points. BEVFormer [145] generates dense queries from BEV grids. TransFusion [6] produces object queries from initial detections and applies cross-attention to LiDAR and image features in a Transformer decoder. UVTR [139] fuses object queries with image and LiDAR voxels in a Transformer decoder. FUTR3D [43] fuses object queries with features from different sensors in a unified way.

In the third stage, many papers try to apply the designs of Vision Transformers to 3D object detectors. Following [63, 168], they split inputs into patches and apply self-attention within each patch and across different patches. SST [70] proposes a sparse Transformer, in which voxels in a local region are grouped into a patch and sparse regional attention is applied to the voxels in a patch, and then region shift is applied to change the grouping so new patches can be generated. SWFormer [270] improves [70] with multi-scale feature fusion and voxel diffusion.

### 6.2 Transformer applications in 3D object detection

**Applications of Transformer-based 3D detectors.** Transformer architectures have been broadly adopted in various types of 3D object detectors. For point-based 3D object detectors, a point-based Transformer [208] has been developed to replace the conventional PointNet backbone. For voxel-based 3D detectors, a lot of papers [187, 70, 270] propose novel voxel-based Transformers to replace the conventional convolutional backbone. For point-voxel based 3D object detectors, a new Transformer-based detection head [250] has been proposed for better proposal refinement. For monocular 3D object detectors, Transformers can be used to fuse image and depth features [107]. For multi-view 3D object detectors, Transformers are utilized to fuse multi-view image features for each query [145, 305]. For multi-modal 3D object detectors, many papers [6, 139, 43] leverage Transformer architectures and special cross-attention mechanisms to fuse features of different modalities. For temporal 3D object detectors, Temporal-Channel Transformer [357] is proposed to model temporal relationships across LiDAR frames.

## 7 Temporal 3D Object Detection

In this section, we introduce the temporal 3D object detection methods. Based on the data types, these methods can be divided into three categories: detection from LiDAR sequences, detection from streaming inputs, and detection from videos. In Section 7.1, we review the 3D object detection methods leveraging sequential LiDAR sweeps. In Section 7.2, we introduce the detection approaches with streaming data as input. In Section 7.3, we investigate 3D detection from videos and multi-modal temporal data. A chronological overview of the temporal detection approaches is shown in Figure 21 and a taxonomy is in Table 14.

Fig. 21: Chronological overview of the temporal 3D object detection methods.

Table 14: A taxonomy of temporal 3D object detection methods based on input representations.

| Input                          | Methods                              |
| ------------------------------ | ------------------------------------ |
| LiDAR multi-frame point clouds | [108, 343, 372, 349, 357] [229, 337] |
| LiDAR multi-frame range images | [193, 123]                           |
| LiDAR streaming inputs         | [92, 76, 37]                         |
| Camera videos                  | [100, 14, 222]                       |

Fig. 22: An illustration of detection from LiDAR sequences.

### 7.1 3D object detection from LiDAR sequences

**Problem and Challenge.** While most methods focus on detection from a single-frame point cloud, there also exist many approaches leveraging multi-frame point clouds for more accurate 3D object detection. These methods are trying to tackle the temporal detection problem by fusing multi-frame features via various temporal modeling tools, and they can also obtain more complete 3D shapes by merging multi-frame object points into a single frame. Temporal 3D object detection has exhibited great success in offline 3D auto-labeling pipelines. However, in onboard applications, these methods still suffer from memory and latency issues, as processing multiple frames inevitably brings additional time and memory costs, which can become severe when models are running on embedded devices. An illustration of temporal 3D object detection from LiDAR sequences is shown in Figure 22.

**3D object detection from sequential sweeps.** Most detection approaches using multi-frame point clouds resort to proposal-level temporal information aggregation. Namely, 3D object proposals are first generated independently from each frame of point cloud through a shared detector, and then various temporal modules are applied on the object proposals and the respective RoI features to aggregate the information of objects across different frames. The adopted temporal aggregation modules include temporal attention [343], ConvGRU [349], graph network [372], LSTM [108], and Transformer [357]. Temporal 3D object detection is also applied in the 3D object auto-labeling pipelines [229, 337]. In addition to temporal detection from multi-frame point clouds, there are also some works [193, 123] leveraging sequential range images for 3D object detection.

### 7.2 3D object detection from streaming data

**Problem and Challenge.** Point clouds collected by rotating LiDARs are intrinsically a streaming data source in which LiDAR packets are sequentially recorded in a sweep. It typically takes 50-100 ms for a rotating LiDAR sensor to generate a \(360^{\circ}\) complete LiDAR sweep, which means that by the time a point cloud is produced, it no longer accurately reflects the scene at the exact time. This poses a challenge to autonomous driving applications which generally require minimal reaction times to guarantee driving safety. Many endeavors have been made to directly detect 3D objects from the streaming data. These methods generally detect 3D objects on the active LiDAR packets immediately without waiting for the full sweep to be built. Streaming 3D object detection is a more accurate and low-latency solution to vehicle perception compared to detection from full LiDAR sweeps. An illustration of 3D object detection from streaming data is shown in Figure 23.

Fig. 23: An illustration of streaming 3D object detection. Reference: [76] and [37].

**Streaming 3D object detection.** Similar to temporal detection from multi-frame point clouds, streaming detection methods [92] can treat each LiDAR packet as an independent sample to detect 3D objects and apply temporal modules on the sequential packets to learn the inter-packets relationships. However, a LiDAR packet normally contains an incomplete point cloud and the information from a single packet is generally not sufficient for accurately detecting 3D objects. To this end, some papers try to provide more context information for detection in a single packet. The proposed techniques include a spatial memory bank [76] and a multi-scale context padding scheme [37].

### 7.3 3D object detection from videos

**Problem and Challenge.** Video is an important data type and can be easily obtained in autonomous driving applications. Compared to single-image based 3D object detection, video-based 3D detection naturally benefits from the temporal relationships of sequential images. While numerous works focus on single-image based 3D object detection, only a few papers investigate the problem of 3D object detection from videos, which leaves an open challenge to the research community.

**Video-based 3D object detection.** Video-based detection approaches generally extend the image-based 3D object detectors by tracking and fusing the same objects across different frames. The proposed trackers include LSTM [100] and the 3D Kalman filter [14]. In addition, there are some works [222, 365] leveraging both videos and multi-frame point clouds for more accurate 3D object detection. Those methods propose 4D sensor-time fusion to learn features from both temporal and multi-modal data.

## 8 Label-Efficient 3D Object Detection

In this section, we introduce the methods of label-efficient 3D object detection. In previous sections, we generally assume the 3D detectors are trained under full supervision on a specific data domain and with a sufficient amount of annotations. However, in real-world applications, the 3D object detection methods inevitably face the problems of poor generalizability and lacking annotations. To address these issues, label-efficient techniques can be employed in 3D object detection, including domain adaptation (Section 8.1), weakly-supervised learning (Section 8.2), semi-supervised learning (Section 8.3), and self-supervised learning (Section 8.4) for 3D object detection. We will introduce those techniques in the following sections.

Fig. 24: An illustration of domain gaps in 3D detection.

### 8.1 Domain adaptation for 3D object detection

**Problem and Challenge.** Domain gaps are ubiquitous in the data collection process. Different sensor settings and placements, different geographical locations, and different weathers will result in completely different data domains. In most conditions, 3D object detectors trained on a certain domain cannot perform well on other domains. Many techniques have been proposed to address the domain adaptation problem for 3D object detection, e.g. leveraging consistency between source and target domains, and self-training on target domains. Nevertheless, most methods only focus on solving one specific domain transfer problem. Designing a domain adaptation approach that can be generally applied in any domain transfer tasks in 3d object detection will be a promising research direction. An illustration of the domain gaps in 3D object detection is shown in Figure 24 and a taxonomy of the domain adaptive methods is in Table 15

Table 15: A taxonomy of domain adaptation methods for 3D object detection based on transferred domains and techniques.

| Method                | Transferred Domain | Technique                 |
| --------------------- | ------------------ | ------------------------- |
| Wang et al. [301]     | cross-sensor       | statistics normalization  |
| SF-UDA3D [248]        | cross-sensor       | self-training             |
| ST3D [338]            | cross-sensor       | self-training             |
| FAST3D [77]           | cross-sensor       | self-training             |
| SRDAN [366]           | cross-sensor       | domain alignments         |
| MLC-Net [175]         | cross-sensor       | domain alignments         |
| 3D-CoCo [348]         | cross-sensor       | domain alignments         |
| Rist et al. [240]     | cross-sensor       | multi-task learning       |
| PIT [87]              | cross-sensor       | image transform           |
| SPG [329]             | cross-weather      | semantic point generation |
| Saleh et al. [247]    | sim-to-real        | Cycle GAN                 |
| DeBortoli et al. [55] | sim-to-real        | adversarial training      |

**Cross-sensor domain adaptation.** Different datasets have different sensory settings, e.g. a 32-beam LiDAR sensor used in nuScenes [15] versus a 64-beam LiDAR sensor in KITTI [82], and the data is also collected at different geographic locations, e.g. KITTI [82] is collected in Germany while Waymo [268] is collected in United States. These factors will lead to severe domain gaps between different datasets, and the detectors trained on a dataset generally exhibit quite poor performance when they are tested on other datasets. [301] is a notable work that observes the domain gaps between datasets, and they introduce a statistic normalization approach to handle the gaps. Many following works leverage self-training to resolve the domain adaptation problem. In those methods, a detector pre-trained on the source dataset will produce pseudo labels for the target dataset, and then the detector is re-trained on the target dataset with pseudo labels. These methods make improvements mainly on obtaining pseudo labels of higher quality, e.g. [248] proposes a scale-and-detect strategy, [338] introduces a memory bank, [77] leverages the scene flow information, and [355] exploits playbacks to enhance the quality of pseudo labels. In addition to the self-training approaches, there also exist some papers building alignments between source and target domains. The domain alignments can be established through a scale-aware and range-aware alignment strategy [366], multi-level consistency [175], and a contrastive co-training scheme [348].

In addition to the domain gaps among datasets, different sensors also produce data of distinct characteristics. A 32-beam LiDAR produces much sparser point clouds compared to a 64-beam LiDAR, and images obtained from different cameras also have diverse sizes and intrinsics. [240] introduces a multi-task learning scheme to tackle the domain gaps between different LiDAR sensors, and [87] proposes the position-invariant transform to address the domain gaps between different cameras.

**Cross-weather domain adaptation.** Weather conditions have a huge impact on the quality of collected data. On rainy days, raindrops will change the surface property of objects so that fewer LiDAR beams can be reflected and detected, so point clouds collected on rainy days are much sparser than those obtained under dry weather. Besides fewer reflections, rain also causes false positive reflections from raindrops in mid-air. [329] addresses the cross-weather domain adaptation problem with a novel semantic point generation scheme.

**Sim-to-real domain adaptation.** Simulated data has been broadly adopted in 3D object detection, as the collected real-world data cannot cover all driving scenarios. However, the synthetic data has quite different characteristics from the real-world data, which gives rise to a sim-to-real adaptation problem. Many approaches are proposed to resolve this problem, including GAN [386] based training [247] and introducing an adversarial discriminator [55] to distinguish real and synthetic data.

### 8.2 Weakly-supervised 3D object detection

**Problem and Challenge.** Existing 3D object detection methods highly rely on training with vast amounts of manually labeled 3D bounding boxes, but annotating those 3D boxes is quite laborious and expensive. Weakly-supervised learning can be a promising solution to this problem, in which weak supervisory signals, e.g. less expensive 2D annotations, are exploited to train the 3D object detection models. Weakly-supervised 3D object detection requires fewer human efforts for data annotation, but there still exists a non-negligible performance gap between the weakly-supervised and the fully-supervised methods. An illustration of weakly-supervised 3D object detection is shown in Figure 25.

Fig. 25: An illustration of weakly-supervised 3D detection.

**Weakly-supervised 3D object detection.** Weakly-supervised approaches leverage weak supervision instead of fully annotated 3D bounding boxes to train 3D object detectors. The weak supervisions include 2D image bounding boxes [311, 215], a pretrained image detector [235], BEV object centers and vehicle instances [189, 190]. Those methods generally design novel learning mechanisms to skip the 3D box supervision and learn to detect 3D objects by mining useful information from weak signals.

### 8.3 Semi-supervised 3D object detection

**Problem and Challenge.** In real-world applications, data annotation requires much more human effort than data collection. Typically a data acquisition vehicle can collect more than 100k frames of point clouds in a day, while a skilled human annotator can only annotate 100-1k frames per day. This will inevitably lead to a rapid accumulation of a large amount of unlabeled data. Hence how to mine useful information from largescale unlabeled data has become a critical challenge to both the research community and the industry. Semi-supervised learning, which exploits a small amount of labeled data and a huge amount of unlabeled data to jointly train a stronger model, is a promising direction. Combining 3D object detection with semi-supervised learning can boost detection performance. An illustration of semi-supervised 3D object detection is shown in Figure 26.

Fig. 26: An illustration of semi-supervised 3D detection.

**Semi-supervised 3D object detection.** There are mainly two categories of approaches in semi-supervised 3D object detection: pseudo-labeling and teacher-student learning. The pseudo labeling approaches [18, 284] first train a 3D object detector with the labeled data, and then use the 3D detector to produce pseudo labels for the unlabeled data. Finally, the 3D object detector is re-trained with the pseudo labels on the unlabeled domain. The teacher-student methods [377] adapt the Mean Teacher [274] training paradigm to 3D object detection. Specifically, a teacher detector is first trained on the labeled domain, and then the teacher detector guides the training of a student detector on the unlabeled domain by encouraging the output consistencies between the two detection models.

Fig. 27: An illustration of self-supervised 3D detection.

### 8.4 Self-supervised 3D object detection

**Problem and Challenge.** Self-supervised pre-training has become a powerful tool when there exists a large amount of unlabeled data and limited labeled data. In self-supervised learning, models are first pre-trained on large-scale unlabeled data and then fine-tuned on the labeled set to obtain a better performance. In autonomous driving scenarios, self-supervised pretraining for 3D object detection has not been widely explored. Existing methods are trying to adapt the self-supervised methods, e.g. contrastive learning, to the 3D object detection problem, but the rich semantic information in multi-modal data has not been well exploited. How to effectively handle the raw point clouds and images to pre-train an effective 3D object detector remains an open challenge. An illustration of self-supervised 3D object detection is in Figure 27.

**Self-supervised 3D object detection.** Self-supervised methods generally apply the contrastive learning techniques [96, 42] to 3D object detection. Specifically, an input point cloud is first transformed into two views with augmentations, and then contrastive learning is employed to encourage the feature consistencies of the same 3D locations across the two views. Finally, the 3D detector pre-trained with contrastive learning is further fine-tuned on the labeled set to attain better performance. PointContrast [325] first introduces the contrastive learning paradigm in 3D object detection, and the following papers improve this paradigm by leveraging the depth information [374] and clustering [146]. In addition to self-supervised learning for point cloud detectors, there are also some works trying to exploit both point clouds and images for self-supervised 3D detection, e.g. [143] proposes an intra-modal and inter-modal contrastive learning scheme on the multi-modal inputs.

## 9 3D Object Detection in Driving Systems

In this section, we introduce some critical problems of 3D object detection in driving systems. In Section 9.1, we review and analyze the approaches in which 3D object detection is trained together with other tasks, e.g. tracking, trajectory prediction, motion planning, localization, in an end-to-end manner. In Section 9.2, we introduce the simulation systems designed for 3D object detection and autonomous driving. In Section 9.3, we investigate the research topics on the robustness of 3D object detectors and safety-aware 3D object detection. In Section 9.4, we review the approaches of collaborative 3D object detection.

### 9.1 End-to-end learning for autonomous driving

**Problem and Challenge.** 3D object detection is a critical component of perception systems, and the performance of 3D object detectors will have a profound influence on downstream tasks like tracking, prediction, and planning. Hence from the systematic perspective, jointly training 3D object detection models with other perception tasks as well as the downstream tasks will be a better solution to autonomous driving. An open challenge is how to involve all driving tasks in a unified framework and jointly train these tasks in an end-to-end manner. An illustration of end-to-end autonomous driving is shown in Figure 28.

Fig. 28: An illustration of the autonomous driving pipeline. Point cloud and map samples are from [22].

**Joint perception and prediction.** There are many works learning to perceive and track 3D objects and then predict their future trajectories in an end-to-end manner. FaF [174] is a seminal work that proposes to jointly reason about 3D object detection, tracking, and trajectory prediction with a single 3D convolutional network. This design paradigm is followed by a lot of papers with improvements, e.g. [22] leverages the map information, [132] introduces an interactive Transformer, [373] designs a spatialtemporal-interactive network, [318] proposes a spatio-temporal pyramid network, [149] conducts all the tasks in a loop, [221] involves the localization task into the system.

**Joint perception, prediction, and planning.** Many endeavors have been made to involve perception, prediction, and planning in a unified framework. Compared to the joint perception and prediction approaches, the whole system can benefit from the planner's feedback by adding motion planning to the end-to-end pipeline. Many techniques have been proposed to improve this framework, e.g. [246] introduces a semantic occupancy map to produce interpretable intermediate representations, [310] incorporates spatial attention into the framework, [363] proposes a deep structured network, [23] proposes a map-free approach, [53] produces a diverse set of future trajectories.

**End-to-end learning for autonomous driving.** Some methods try to build a completely end-to-end autonomous driving system, in which an autonomous vehicle takes sensory inputs and sequentially performs perception, prediction, planning, and motion control in a loop, and finally produces steering and speed signals for driving. [12] first introduces the idea and implements the image-based end-to-end driving system with a convolutional neural network. [322] proposes an end-to-end architecture with multi-modal inputs. [52] and [113] propose to learn end-to-end driving systems with conditional imitation learning and deep reinforcement learning respectively.

### 9.2 Simulation for 3D object detection

**Problem and Challenge.** 3D object detection models generally require a large amount of data for training. While the data can be collected in real-world scenarios, the real-world data generally suffers from a long-tail distribution. For example, the scenarios of traffic accidents or extreme weather are seldom recorded but are quite important for training a robust 3D object detector. Simulation is a promising solution to address the long tail data distribution problem, as we can create synthetic data for those rare but critical scenarios. An open challenge for simulation is how to create more realistic synthetic data.

**Visual simulation.** Many endeavors have been made to generate photo-realistic synthetic images in driving scenarios. The ideas of those methods include leveraging a graphics engine [1, 243], exploiting texture-mapped surfels [341], leveraging real-world data [48], and learning a controllable neural simulator [115].

**LiDAR simulation.** In addition to generating synthetic images, many approaches try to generate LiDAR point clouds by simulation. Some methods [71, 202, 73] propose novel point cloud rendering mechanisms by simulating the real-world effects. Some approaches [183] leverage real-world instances to reconstruct 3D scenes. Other papers focus on simulation for safety-critical scenarios [286] or under adverse weather conditions [91].

**Driving simulation.** Many papers try to build an interactive driving simulation platform where a virtual vehicle can perceive and interact with the virtual environments and finally plan the maneuvers. CARLA [62] is a pioneering open-source simulator for autonomous driving. Other papers utilize a graphics engine [249], leverage real-world data [16], or develop a data-driven method [4] for driving simulation. There are also some works simulating the traffic flows [272, 271] or testing the safety of vehicles by simulation [316].

### 9.3 Robustness for 3D object detection

**Problem and Challenge.** Learning-based 3D object detectors are generally vulnerable to adversarial attacks. Adding perturbations or objects to the sensory inputs in an adversarial manner can fool the perception models and lead to misdetections. An open challenge of robust 3D object detection is to develop practical adversarial attack and defense algorithms that can be easy to implement and can be applied to most detection models.

**Adversarial attacks on the LiDAR sensors.** Many endeavors have been made to attack the LiDAR sensors and fool the LiDAR-based perception models with adversarial machine learning. Cao et al. [19] attack the LiDAR sensor and spoof obstacles close to the front of a victim autonomous vehicle. To achieve this goal, they introduce a novel algorithm to strategically control the spoofed attack to fool the LiDAR-based 3D object detection model. Wicker et al. [314] study the problem of adversarial attacks on the point-based detection models. They propose an iterative saliency occlusion approach to generate adversarial point cloud examples by dropping critical points. Tu et al. [276] propose a method to generate physically realizable adversarial examples that can be placed on a vehicle and make this vehicle invisible to the LiDAR-based 3D object detectors. Sun et al. [266] study the general vulnerability of current LiDAR-based 3D object detection models and identify the ignored occlusion patterns in LiDAR point clouds that make vehicles vulnerable to spoofing attacks. They further propose a black-box spoofing attack method that can fool all target detection models. Zhu et al. [389] propose to use arbitrary objects to attack LiDAR-based 3D object detection models. Towards this goal, they introduce a method to identify the adversarial locations in a 3D scene, so that arbitrary objects placed at these locations can fool the LiDAR perception systems. Li et al. [137] exploit the fact that LiDAR point clouds collected from a moving vehicle need calibration based on the moving trajectories, so they propose to spoof the vehicle's trajectory with adversarial perturbations, which can distort the LiDAR sweeps and fool the 3D object detectors. Tu et al. [277] perform adversarial attacks on the LiDAR perception models under the setting of multi-agent collaborative perception. Specifically, they fool the perception model of an agent by sending an adversarial message from the attacker in the multi-agent communication system.

**Adversarial attacks on the multi-modal sensory inputs.** In addition to attacking the LiDAR-based perception models, there exist some works trying to perform adversarial attacks on both cameras and LiDAR sensors simultaneously. Cao et al. [20] propose to generate a physically-realizable and adversarial 3D object that is invisible to both the camera and LiDAR sensor. The adversarial object is generated through optimization and can be leveraged to attack the multi-sensor fusion-based 3D object detection models. Tu et al. [278] perform adversarial attacks on multi-modal perception models by introducing an adversarial textured mesh that can be placed on a vehicle and make this vehicle invisible to the multi-modal perception models. Specifically, the adversarial mesh is first rendered into both LiDAR points and image pixels in a differentiable manner, and then the multimodal inputs are passed through a fusion-based detector. Finally, an adversarial loss is employed to adjust the mesh parameters.

### 9.4 Collaborative 3D object detection

**Problem and Challenge.** Existing 3D detection approaches are mainly based on a single ego-vehicle. However, detecting 3D objects with a single vehicle inevitably meets two challenges: occlusion and sparsity of the far-away objects. To this end, some papers resort to detection under the multi-agent collaborative setting, where an ego-vehicle can communicate with other agents, e.g. vehicles or infrastructures, and exploit the information from other agents to improve the perception accuracy. A challenge of collaborative perception is how to properly balance the accuracy improvements and the communication bandwidth requirements.

**Collaborative 3D object detection.** Collaborative detection approaches fuse the information from multiple agents to boost the performance of a 3D object detector. The fused information can be raw sensory inputs from other agents [34, 367], which cost little communication bandwidth and is quite efficient for detection, and it can also be compressed feature maps [33, 295, 279, 136], which cost non-negligible communication bandwidth but generally lead to better detection performance. There are also some papers studying when to communicate with other agents [163] and which agent to communicate [164].

## 10 Analysis and Outlooks

In this section, we conduct a systematic comparison and analysis of the 3D object detection approaches and prospect the future research directions of 3D object detection for autonomous driving. In Section 10.1, we conduct a comprehensive analysis of the detection performances and the inference speeds of various 3D object detection methods, i.e. LiDAR-based, camera-based, multi-modal approaches, on multiple datasets, from which we further summarize the research trends over the years. In Section 10.2, we propose future research directions in this area.

### 10.1 Research trends

We comprehensively collect the statistics of various types of 3D object detection methods in recent years. The statistics include performances and inference time of the 3D object detectors on the most broadly-adopted KITTI [82], nuScenes [15], and Waymo [268] dataset. Table 16, Table 17 and Table 18 show the statistical data. By analyzing these data, we obtain some intriguing findings on the research trends of 3D object detection.

#### 10.1.1 Trends of dataset selection

Before 2018, most methods were evaluated on the KITTI dataset, and the evaluation metric they adopted is 2D average precision \((AP*{2D})\) , where they project the 3D bounding boxes into the image plane and compare them with the ground truth 2D boxes. From 2018 until now, more and more papers have adopted the 3D or BEV average precision \((AP*{3D}\) or \(AP*{BEV}\) ), which is a more direct metric to measure 3D detection quality. For the LiDAR-based methods, the detection performances on KITTI quickly get converged over the years, e.g. \(AP*{3D}\) of easy cases increases from \(71.40\%\) [339] to \(90.90\%\) [255], and even \(AP*{3D}\) of hard cases reaches \(79.14\%\) [187]. Therefore, since 2019, more and more LiDAR-based approaches have turned to larger and more diverse datasets, such as the nuScenes dataset and the Waymo Open dataset. Large-scale datasets also provide more useful data types, e.g. raw range images provided by Waymo facilitate the development of range-based methods. For the camera-based detection methods, \(AP*{3D}\) of monocular detection on KITTI increases from \(1.32\%\) [241] to \(23.22\%\) [211], leaving huge room for improvement. Until now, only a few monocular methods have been evaluated on the Waymo dataset. For the multi-modal detection approaches, the methods before 2019 are mostly tested on the KITTI dataset, and after that most papers resort to the nuScenes dataset, as it provides more multi-modal data.

#### 10.1.2 Trends of inference time

PointPillars [124] has achieved remarkable inference speed with only 16ms latency, and its architecture has been adopted by many following works [350, 302, 251]. However, even with the emergence of more powerful hardware, the inference speed didn't exhibit a significant improvement over the years. This is mainly because most methods focus on performance improvement and pay less attention to efficient inference. Many papers have introduced new modules into the existing detection pipelines, which also brings additional time costs. For the pseudo-LiDAR based detection methods, the stereo-based methods, and most multimodal methods, the inference time is generally more than 100 ms, which cannot satisfy the real-time requirement and hampers the deployment in real-world applications.

#### 10.1.3 Trends of the LiDAR-based methods

LiDAR-based 3D object detection has witnessed great advances in recent years. Among the LiDAR-based methods, the voxel-based and point-voxel based detection approaches attain superior performances, e.g. [187] attains \(82.09\%\) moderate \(AP*{3D}\) and [253] obtains \(90.25\%\) easy \(AP*{3D}\) on the KITTI dataset. The pillar-based detection methods are extremely fast, e.g. [124] runs at \(60\mathrm{Hz}\) , but the detection accuracy is generally worse than the voxel-based methods. The range-based and BEV-based approaches are also quite efficient, e.g. [335] and [192] only requires \(30\mathrm{ms}\) for one-pass inference. The point-based detectors can obtain a good performance, but their inference speeds are greatly influenced by the choices of sampling and operators.

For point-based 3D object detectors, moderate AP has been increasing from \(53.46\%\) [252] to \(79.57\%\) [256] on the KITTI benchmark. The performance improvements are mainly owing to two factors: more robust point cloud samplers and more powerful point cloud operators. The development of point cloud samplers starts with Farthest Point Sampling (FPS) [252, 340], and many following point cloud detectors have been improving point cloud samplers based on FPS, including fusion-based FPS [342], target-based FPS [203], FPS with coordinates refinement [208]. A good point cloud sampler could produce candidate points that have better coverage of the whole scene, so it avoids missing detections when the point cloud is sparse, which helps improve the detection performance. Besides point cloud samplers, point cloud operators have also progressed rapidly, from the standard set abstraction [252, 339, 340, 342] to graph operators [256, 203] and Transformers [208]. Point cloud operators are crucial for extracting powerful feature representations from point clouds. Hence powerful point cloud operators can help detectors better obtain semantic information about 3D objects and improve performance.

For grid-based 3D object detectors, moderate AP has been increasing from \(50.81\%\) [10] to \(82.09\%\) [187] on the KITTI benchmark. The performance improvements are mainly driven by better backbone networks and detection heads. The development of backbone networks has experienced four stages: (1) 2D networks to process BEV images that are generated by point cloud projection [10, 335], (2) 2D networks to process pillars that are generated by PointNet encoding [124], (3) 3D sparse convolutional networks to process voxelized point clouds [382], (4) Transformer-based architectures [187, 70, 270]. The trend of backbone designs is to encode more 3D information from point clouds, which leads to more powerful BEV representations and better detection performance, but those early designs are still popular due to efficiency. Detection head designs have experienced the transition from anchor-based heads [333] to center-based heads [350], and the object localization ability has been improved with the development of detection heads. Other head designs such as IoU rectification [375] and sequential head [332] can further boost performance.

For point-voxel based 3D object detectors, moderate AP has been increasing from \(75.73\%\) [44] to \(82.08\%\) [185] on the KITTI benchmark. The performance improvements come from more power operators [165, 94] and modules [253, 255, 185, 250] that can effectively fuse point and voxel features.

For range-based 3D object detectors, L1 mAP has been increasing from \(52.11\%\) [192] to \(78.4\%\) [269] on the Waymo Open dataset. The performance improvements come from designs of specialized operators [11, 69, 27] that can handle range images more effectively, as well as view transforms and multi-view aggregation [152, 153, 269].

#### 10.1.4 Trends of the camera-based methods

Camera-based 3D object detection has shown rapid progress recently. Among the camera-based methods, the stereo-based detection methods generally outperform the monocular detection approaches by a large margin. For example, the state-of-theart stereo-based method [89] attains \(64.66\%\) moderate \(AP*{3D}\) while the state-of-the-art monocular method [211] only achieves \(16.34\%\) moderate \(AP*{3D}\) . This is mainly because depth and disparity estimated from stereo images are much more accurate than those estimated from monocular images, and accurate depth estimation is the most important factor in camera-based 3D object detection. Multi-camera 3D object detection has been progressing fast with the emergence of BEV perception and Transformers. State-of-the-art method [212] attains \(54.0\%\) mAP and \(61.9\) NDS on nuScenes, which has outperformed some prestigious LiDAR-based 3D object detectors [124].

For monocular 3D object detectors, moderate AP has been increasing from \(1.51\%\) [159] to \(16.34\%\) [211] on the KITTI benchmark. The major challenge of monocular 3D object detection is how to obtain accurate 3D information from a single 2D image, as localization errors dominate detection errors. The performance improvements are driven by more accurate depth prediction, which can be achieved by better network architecture designs [13, 293, 380, 182], leveraging depth images [326] or pseudo-LiDAR point clouds [299, 354], introducing geometry constraints [197, 17, 39, 47], and 3D object reconstruction [31, 359, 319, 122].

For stereo-based 3D object detectors, moderate AP has been increasing from \(4.37\%\) [234] to \(64.66\%\) [89] on the KITTI benchmark. The performance improvements mainly come from better network designs and data representations. Early works [134] rely on stereo-based 2D detection networks to produce paired object bounding boxes and then predict object-centric stereo/depth information with a sub-network. However, those object-centric methods generally lack global disparity information which hampers accurate 3D detection in a scene. Later on, pseudo-LiDAR based approaches [299] generate disparity maps from stereo images and then transform disparity maps into 3D pseudo-LiDAR point clouds that are finally passed to a LiDAR detector to perform 3D detection. The transformation from 2D disparity maps to 3D point clouds is crucial and can significantly boost 3D detection performance. Many following papers are based on the pseudo-LiDAR paradigm and improve it with stronger stereo matching network [354] and end-to-end training of stereo matching and LiDAR detection [231]. Recent methods [304, 46] transforms disparity maps into 3D volumes and apply grid-based detectors on the volumes, which results in better performance.

For multi-view 3D object detection, mAP has been increasing from \(41.2\%\) [305] to \(54.0\%\) [212] on the nuScenes dataset. For BEV-based approaches, the performance improvements are mainly from better depth prediction [140, 138]. More accurate depth information results in more accurate camera-to-BEV transformation so detection performance can be improved. For querybased methods, the performance improvements come from better designs of 3D object queries [145], more powerful image features [162], and new attention mechanisms [61].

#### 10.1.5 Trends of the multi-modal methods

The multi-modal methods generally exhibit a performance improvement over the single-modal baselines but at the cost of introducing additional inference time. For instance, the multimodal detector [282] outperforms the LiDAR baseline [350] by \(8.8\%\) mAP on nuScenes, but the inference time of [282] also increases to \(542~\mathrm{ms}\) compared to the baseline \(70~\mathrm{ms}\) . The problem can be more severe in the early-fusion based approaches, where the 2D networks and the 3D detection networks are connected in a sequential manner. Most multi-modal detection methods are designed and tested on the KITTI dataset, in which only a frontview image and the corresponding point cloud are utilized. Recently more and more methods are proposed and evaluated on the nuScenes dataset, in which multi-view images, point clouds, and high-definition maps are provided.

For early-fusion based methods, moderate AP increases from \(70.39\%\) [226] to \(76.51\%\) [306] on the KITTI benchmark, and mAP increases from \(46.4\%\) [281] to \(66.8\%\) [282] on nuScenes dataset. There are two crucial factors that contribute to the performance increase: knowledge fusion and data augmentation. From the results, we can observe that point-level knowledge fusion [281, 330] is generally more effective than region-level fusion [226, 306]. This is because region-level knowledge fusion simply reduces the detection range, while point-level knowledge fusion can provide fine-grained semantic information which is more beneficial in 3D detection. Besides, consistent data augmentations between point clouds and images [282] can also significantly boost detection performance.

For intermediate and late fusion based methods, moderate AP increases from \(62.35\%\) [41] to \(80.67\%\) [209] on the KITTI benchmark, and mAP increases from \(52.7\%\) [353] to \(69.2\%\) [170] on the nuScenes dataset. Most methods focus on three critical problems: where to fuse different data representations, how to fuse these representations, and how to build reliable alignments between points and image pixels. For the where-to-fuse problem, different approaches try to fuse image and LiDAR features at different places, e.g. 3D backbone networks, BEV feature maps, RoI heads, and outputs. From the results we can observe that fusion at any place can boost detection performance over single-modality baselines, and fusion in the BEV space [170, 150, 6] is more popular recently for its performance and efficiency. For the how-to-fuse problem, the development of fusion operators has experienced simple concatenation [117], continuous convolutions [148, 147], attention [353, 109], and Transformers [6, 139, 43], and fusion with Transformers exhibit prominent performance on all benchmarks. For the point-to-pixel alignment problem, most papers reply on fixed extrinsics and intrinsics to construct point-to-pixel correspondences. However, due to occlusion and calibration errors, those correspondences can be noisy and misalignment will harm performance. Recent works [170] circumvent this problem by directly fusing camera and LiDAR BEV feature maps, which is more robust to noise.

#### 10.1.6 Systematic comparisons

Considering all the input sensors and modalities, LiDAR-based detection is the best solution to the 3D object detection problem, in terms of both speed and accuracy. For instance, [350] achieves 80.28% moderate \(AP*{3D}\) and still runs at 30 FPS on KITTI. Multi-modal detection is built upon LiDAR-based detection, and can obtain a better detection performance compared to the LiDAR baselines, becoming state-of-the-art in terms of accuracy. Camera-based 3D object detection is a much cheaper and quite efficient solution in contrast to LiDAR and multi-modal detection. Nevertheless, the camera-based methods generally have a worse detection performance due to inaccurate depth predictions from images. The state-of-the-art monocular [211] and stereo [89] detection approach only obtain \(16.34\%\) and \(64.66\%\) moderate \(AP*{3D}\) respectively on KITTI. Recent advances in multi-view 3D object detection are quite promising. The state-of-the-art [212] achieves \(54.0\%\) mAP on nuScenes, which could perform on par with some classic LiDAR detectors [333]. In conclusion, LiDAR-based and multi-modal detectors are the best solutions considering speed and accuracy as the dominant factors, while camera-based detectors can be the best choice considering cost as the most important factor, and multi-view 3D detectors are becoming promising and may outperform LiDAR detectors in the future.

### 10.2 Future outlooks

With all the reviewed literature and the analysis of research trends over the past years, we can now make some predictions on the future research directions of 3D object detection.

#### 10.2.1 Open-set 3D object detection

Nearly all existing works are proposed and evaluated on close datasets, in which the data only covers limited driving scenarios and the annotations only include basic classes, e.g. cars, pedestrians, cyclists. Although those datasets can be large and diverse, they are still not sufficient for real-world applications, in which critical scenarios like traffic accidents and rare classes like unknown obstacles are important but not covered by the existing datasets. Therefore, existing 3D object detectors that are trained on the close sets have a limited capacity of dealing with those critical scenarios and cannot identify the unknown categories. To overcome the above limitations, designing 3D object detectors that can learn from the open world and recognize a wide range of object categories will be a promising research direction. [24] is a good start for open-set 3D object detection and hopefully more methods will be proposed to tackle this problem.

#### 10.2.2 Detection with stronger interpretability

Deep learning based 3D object detection models generally lack interpretability. Namely, some important questions on how the networks can identify 3D objects in point clouds, how occlusion and noise of 3D objects can affect the model outputs, and how much context information is needed for detecting a 3D object, have not been properly answered due to the black-box property of deep neural networks. On the other hand, understanding the behaviors of 3D detectors and answering these questions are quite important if we want to perform 3D object detection in a more robust manner and avoid those unexpected cases brought by black-box detectors. Therefore, the methods that can understand and interpret the existing 3D object detection models will be appealing in future research.

#### 10.2.3 Efficient hardware design for 3D object detection

Most existing works focus on designing algorithms to tackle the 3D object detection problem, and their models generally run on GPUs. Nevertheless, unlike image operators that are highly optimized for GPU devices, point clouds and voxels are sparse and irregular, and the commonly adopted 3D operators like set abstraction or 3D sparse convolutions are not well suited for GPUs. Hence those LiDAR object detectors cannot run as efficiently as the image detectors on the existing hardware devices. To handle this challenge, designing novel devices where the hardware architectures are optimized for 3D operators as well as the task of 3D object detection will be an important research direction and will be beneficial for real-world deployment. [158] is a pioneering hardware work to accelerate point cloud processing, and we believe more and more papers will come in this field. In addition, new sensors, e.g. solid-state LiDARs, LiDARs with doppler, 4D radars, will also inspire the design of 3D object detectors.

#### 10.2.4 Detection in end-to-end self-driving systems

Most existing works treat 3D object detection as an independent task and try to maximize the detection metrics such as average precision. Nevertheless, 3D object detection is closely correlated with other perception tasks as well as downstream tasks such as prediction and planning, so simply pursuing high average precision for 3D object detection may not be optimal when considering the autonomous driving system as a whole. Therefore, conducting 3D object detection and other tasks in an end-to-end manner, and learning 3D detectors from the feedback of planners, will be the future research trends of 3D object detection.

## 11 Conclusion

In this paper, we comprehensively review and analyze various aspects of 3D object detection for autonomous driving. We start from the problem definition, datasets, and evaluation metrics for 3D object detection, and then we introduce various kinds of sensorbased 3D object detection approaches, including LiDAR-based, camera-based, and multi-modal 3D object detection methods. We further investigate 3D object detection leveraging temporal data, with label-efficient learning, as well as its applications in autonomous driving systems. Finally, we summarize the research trends in recent years and prospect the future research directions of 3D object detection.

## 12 Acknowledgements

This project is funded in part by the National Key R&D Program of China Project 2022ZD0161100, by the Centre for Perceptual and Interactive Intelligence (CPII) Ltd under the Innovation and Technology Commission (ITC)'s InnoHK, by General Research Fund Project 14204021 and Research Impact Fund Project R5001-18 of Hong Kong RGC. Hongsheng Li and Xiaogang Wang are PIs of CPII under the InnoHK.

Table 16: A comprehensive performance analysis of various categories of 3D object detection methods across different datasets. We report the inference time (ms) originally reported in the papers, and report \(\mathrm{AP}|_{R_{40}}\) \((\%)\) for 3D car detection ( \(\ast\) denotes \(\mathrm{AP}|_{R_{40}}\) for BEV car detection) on the KITTI test benchmark, mAP \((\%)\) and NDS scores on the nuScenes test set, Level 1 (L1) mAP and Level 2 (L2) mAP on the Waymo validation set. We group the methods based on the sensor types and the input representations, and sort them by the year of publication.

| Method                  | Sensor | Representation | Year | Inference Time (ms) | KITTI Car Easy | KITTI Car Mod. | KITTI Car Hard | nuScenes mAP | nuScenes NDS | Waymo Vehicle L1 | Waymo Vehicle L2 |
| ----------------------- | ------ | -------------- | ---: | ------------------: | -------------: | -------------: | -------------: | -----------: | -----------: | ---------------: | ---------------: |
| IPOD [339]              | LiDAR  | Point          | 2018 |                   - |          71.40 |          53.46 |          48.34 |            - |            - |                - |                - |
| StarNet [203]           | LiDAR  | Point          | 2019 |                   - |          81.63 |          73.99 |          67.07 |            - |            - |             53.7 |                - |
| PointRCNN [252]         | LiDAR  | Point          | 2019 |                 100 |          85.94 |          75.76 |          68.32 |            - |            - |                - |                - |
| STD [340]               | LiDAR  | Point          | 2019 |                  80 |          86.61 |          77.63 |          76.06 |            - |            - |                - |                - |
| 3DSSD [342]             | LiDAR  | Point          | 2020 |                  38 |          88.36 |          79.57 |          74.55 |         42.6 |         56.4 |                - |                - |
| Point-GNN [256]         | LiDAR  | Point          | 2020 |                 640 |          88.33 |          79.47 |          72.29 |            - |            - |                - |                - |
| Pointformer [208]       | LiDAR  | Point          | 2021 |                   - |          87.13 |          77.06 |          69.25 |         53.6 |            - |                - |                - |
| Vote3D [283]            | LiDAR  | Voxel          | 2015 |                 500 |              - |              - |              - |            - |            - |                - |                - |
| Vote3Deep [68]          | LiDAR  | Voxel          | 2017 |                1100 |              - |              - |              - |            - |            - |                - |                - |
| 3D-FCN [125]            | LiDAR  | Voxel          | 2017 |                   - |              - |              - |              - |            - |            - |                - |                - |
| VoxelNet [382]          | LiDAR  | Voxel          | 2018 |                 220 |          77.47 |          65.11 |          57.73 |            - |            - |                - |                - |
| SECOND [333]            | LiDAR  | Voxel          | 2018 |                  50 |          83.13 |          73.66 |          66.20 |            - |            - |                - |                - |
| CBGS [385]              | LiDAR  | Voxel          | 2019 |                   - |              - |              - |              - |         52.8 |         63.3 |                - |                - |
| HVNet [344]             | LiDAR  | Voxel          | 2020 |                  30 |              - |              - |              - |            - |            - |                - |                - |
| DOPS [201]              | LiDAR  | Voxel          | 2020 |                   - |              - |              - |              - |            - |            - |             56.4 |                - |
| MVF [383]               | LiDAR  | Voxel          | 2020 |                   - |              - |              - |              - |            - |            - |            62.93 |                - |
| AFDet [81]              | LiDAR  | Voxel          | 2020 |                   - |              - |              - |              - |            - |            - |            63.69 |                - |
| SSN [388]               | LiDAR  | Voxel          | 2020 |                   - |              - |              - |              - |         46.3 |         56.9 |                - |                - |
| CVC-Net [35]            | LiDAR  | Voxel          | 2020 |                   - |              - |              - |              - |         55.8 |         64.2 |             65.2 |                - |
| Wang et al. [292]       | LiDAR  | Voxel          | 2020 |                  50 |              - |              - |              - |         48.5 |         59.0 |                - |                - |
| SegVoxelNet [347]       | LiDAR  | Voxel          | 2020 |                  40 |          84.19 |          75.81 |          67.80 |            - |            - |                - |                - |
| HotSpotNet [36]         | LiDAR  | Voxel          | 2020 |                  40 |          87.60 |          78.31 |          73.34 |         59.3 |         66.0 |                - |                - |
| Associate-3Ddet [65]    | LiDAR  | Voxel          | 2020 |                  60 |          85.99 |          77.40 |          70.53 |            - |            - |                - |                - |
| TANet [167]             | LiDAR  | Voxel          | 2020 |                   - |          83.81 |          75.38 |          67.66 |            - |            - |                - |                - |
| Part-A2 Net [254]       | LiDAR  | Voxel          | 2020 |                  80 |          85.94 |          77.86 |          72.00 |            - |            - |                - |                - |
| CenterPoint [350]       | LiDAR  | Voxel          | 2021 |                  70 |              - |              - |              - |         58.0 |         65.5 |             76.7 |             68.8 |
| Object DGCNN [297]      | LiDAR  | Voxel          | 2021 |                   - |              - |              - |              - |         58.7 |         66.1 |                - |                - |
| CIA-SSD [375]           | LiDAR  | Voxel          | 2021 |                  30 |          89.59 |          80.28 |          72.87 |            - |            - |                - |                - |
| Voxel R-CNN [57]        | LiDAR  | Voxel          | 2021 |                  40 |          90.90 |          81.62 |          77.06 |            - |            - |            75.59 |            66.59 |
| Voxel Transformer [187] | LiDAR  | Voxel          | 2021 |                 140 |          89.90 |          82.09 |          79.14 |            - |            - |            74.95 |            65.91 |
| SST [70]                | LiDAR  | Voxel          | 2022 |                   - |              - |              - |              - |            - |            - |             74.2 |             65.5 |
| SWFormer [270]          | LiDAR  | Voxel          | 2022 |                   - |              - |              - |              - |            - |            - |             77.8 |             69.2 |
| PointPillars [124]      | LiDAR  | Pillar         | 2019 |                  16 |          79.05 |          74.99 |          68.30 |         40.1 |         55.0 |            56.62 |                - |
| Pillar-OD [302]         | LiDAR  | Pillar         | 2020 |                   - |              - |              - |              - |            - |            - |             69.8 |                - |
| PillarNet [251]         | LiDAR  | Pillar         | 2022 |                   - |              - |              - |              - |         66.0 |         71.4 |            83.23 |            76.09 |
| VeloFCN [126]           | LiDAR  | BEV Image      | 2016 |                1000 |              - |              - |              - |            - |            - |                - |                - |
| BirdNet [10]            | LiDAR  | BEV Image      | 2018 |                   - |        75.52\* |        50.81\* |        50.00\* |            - |            - |                - |                - |
| PIXOR [335]             | LiDAR  | BEV Image      | 2018 |                  35 |        81.70\* |        77.05\* |        72.95\* |            - |            - |                - |                - |
| HDNet [334]             | LiDAR  | BEV Image      | 2018 |                  50 |        89.14\* |        86.57\* |        78.32\* |            - |            - |                - |                - |
| PVCNN [165]             | LiDAR  | Point-Voxel    | 2019 |                  59 |              - |              - |              - |            - |            - |                - |                - |
| Fast Point R-CNN [44]   | LiDAR  | Point-Voxel    | 2019 |                  65 |          84.28 |          75.73 |          67.39 |            - |            - |                - |                - |
| PV-RCNN [253]           | LiDAR  | Point-Voxel    | 2020 |                   - |          90.25 |          81.43 |          76.82 |            - |            - |            77.51 |            68.98 |
| SA-SSD [94]             | LiDAR  | Point-Voxel    | 2020 |                  40 |          88.75 |          79.79 |          74.16 |            - |            - |                - |                - |
| SPVNAS [273]            | LiDAR  | Point-Voxel    | 2020 |                   - |           87.8 |           78.4 |           74.8 |            - |            - |                - |                - |
| InfoFocus [285]         | LiDAR  | Point-Voxel    | 2020 |                   - |              - |              - |              - |         39.5 |            - |                - |                - |
| PVGNet [195]            | LiDAR  | Point-Voxel    | 2021 |                   - |          89.94 |          81.81 |          77.09 |            - |            - |             74.0 |                - |
| HVPR [204]              | LiDAR  | Point-Voxel    | 2021 |                  28 |          86.38 |          77.92 |          73.04 |            - |            - |                - |                - |
| PV-RCNN++ [255]         | LiDAR  | Point-Voxel    | 2021 |                   - |          90.14 |          81.88 |          77.15 |            - |            - |            79.25 |            70.61 |
| CT3D [250]              | LiDAR  | Point-Voxel    | 2021 |                   - |          87.83 |          81.77 |          77.16 |            - |            - |            76.30 |            69.04 |
| LiDAR R-CNN [144]       | LiDAR  | Point-Voxel    | 2021 |                   - |              - |              - |              - |            - |            - |             76.0 |             68.3 |
| Pyramid R-CNN [185]     | LiDAR  | Point-Voxel    | 2021 |                   - |          88.39 |          82.08 |          77.49 |            - |            - |            76.30 |            67.23 |
| LaserNet [192]          | LiDAR  | Range Image    | 2019 |                  30 |              - |              - |              - |            - |            - |            52.11 |                - |
| RCD [11]                | LiDAR  | Range Image    | 2020 |                   - |              - |              - |              - |            - |            - |            69.59 |                - |
| RangeRCNN [152]         | LiDAR  | Range Image    | 2020 |                  45 |          88.47 |          81.33 |          77.09 |            - |            - |            75.43 |                - |
| RangeIoUDet [153]       | LiDAR  | Range Image    | 2021 |                  22 |          88.60 |          79.80 |          76.76 |            - |            - |                - |                - |
| PPC [27]                | LiDAR  | Range Image    | 2021 |                   - |              - |              - |              - |            - |            - |             65.2 |             56.7 |
| RangeDet [69]           | LiDAR  | Range Image    | 2021 |                   - |              - |              - |              - |            - |            - |            72.85 |                - |
| RSN [269]               | LiDAR  | Range Image    | 2021 |                67.5 |              - |              - |              - |            - |            - |             78.4 |             69.5 |
| Mono3D [39]             | Camera | Monocular      | 2016 |                   - |              - |              - |              - |            - |            - |                - |                - |
| Deep3DBox [197]         | Camera | Monocular      | 2017 |                   - |              - |              - |              - |            - |            - |                - |                - |
| Deep MANTA [25]         | Camera | Monocular      | 2017 |                   - |              - |              - |              - |            - |            - |                - |                - |
| SubCNN [320]            | Camera | Monocular      | 2017 |                   - |              - |              - |              - |            - |            - |                - |                - |
| 3D-RCNN [122]           | Camera | Monocular      | 2018 |                   - |              - |              - |              - |            - |            - |                - |                - |
| MultiFusion [326]       | Camera | Monocular      | 2018 |                   - |           7.08 |           5.18 |           4.68 |            - |            - |                - |                - |
| Mono3D++ [98]           | Camera | Monocular      | 2019 |                   - |              - |              - |              - |            - |            - |                - |                - |
| DeepOptics [28]         | Camera | Monocular      | 2019 |                   - |              - |              - |              - |            - |            - |                - |                - |
| Weng et al. [312]       | Camera | Monocular      | 2019 |                   - |              - |              - |              - |            - |            - |                - |                - |
| CenterNet [380]         | Camera | Monocular      | 2019 |                   - |              - |              - |              - |         33.8 |         40.0 |                - |                - |
| OFT-Net [241]           | Camera | Monocular      | 2019 |                 500 |           1.32 |           1.61 |           1.00 |            - |            - |                - |                - |

Table 17: A comprehensive performance analysis of all branches of 3D object detection methods across different datasets. (Continued)

| Method                | Sensor | Representation | Year | Inference Time (ms) | KITTI Car Easy | KITTI Car Mod. | KITTI Car Hard | nuScenes mAP | nuScenes NDS | Waymo Vehicle L1 | Waymo Vehicle L2 |
| --------------------- | ------ | -------------- | ---: | ------------------: | -------------: | -------------: | -------------: | -----------: | -----------: | ---------------: | ---------------: |
| FQNet [159]           | Camera | Monocular      | 2019 |                 500 |           2.77 |           1.51 |           1.01 |            - |            - |                - |                - |
| ROI-10D [182]         | Camera | Monocular      | 2019 |                 200 |           4.32 |           2.02 |           1.46 |            - |            - |                - |                - |
| GS3D [127]            | Camera | Monocular      | 2019 |                   - |           4.47 |           2.90 |           2.47 |            - |            - |                - |                - |
| MonoFENet [7]         | Camera | Monocular      | 2019 |                   - |           8.35 |           5.14 |           4.10 |            - |            - |                - |                - |
| MonoGRNet [233]       | Camera | Monocular      | 2019 |                  60 |           9.61 |           5.74 |           4.25 |            - |            - |                - |                - |
| MonoDIS [261]         | Camera | Monocular      | 2019 |                 100 |          10.37 |           7.94 |           6.40 |         30.4 |         38.4 |                - |                - |
| MonoPSR [118]         | Camera | Monocular      | 2019 |                   - |          10.76 |           7.25 |           5.85 |            - |            - |                - |                - |
| M3D-RPN [13]          | Camera | Monocular      | 2019 |                 160 |          14.76 |           9.71 |           7.42 |            - |            - |                - |                - |
| AM3D [176]            | Camera | Monocular      | 2019 |                 400 |          16.50 |          10.74 |           9.52 |            - |            - |                - |                - |
| SDFLabel [359]        | Camera | Monocular      | 2020 |                   - |              - |              - |              - |            - |            - |                - |                - |
| MonoDR [9]            | Camera | Monocular      | 2020 |                   - |              - |              - |              - |            - |            - |                - |                - |
| Wang et al. [296]     | Camera | Monocular      | 2020 |                   - |              - |              - |              - |            - |            - |                - |                - |
| MoNet3D [381]         | Camera | Monocular      | 2020 |                   - |              - |              - |              - |            - |            - |                - |                - |
| Cai et al. [17]       | Camera | Monocular      | 2020 |                   - |          11.08 |           7.02 |           5.63 |            - |            - |                - |                - |
| MonoPair [47]         | Camera | Monocular      | 2020 |                  60 |          13.04 |           9.99 |           8.65 |            - |            - |                - |                - |
| SMOKE [166]           | Camera | Monocular      | 2020 |                  30 |          14.03 |           9.76 |           7.84 |            - |            - |                - |                - |
| RTM3D [135]           | Camera | Monocular      | 2020 |                   - |          14.41 |          10.34 |           8.77 |            - |            - |                - |                - |
| MoVi-3D [262]         | Camera | Monocular      | 2020 |                   - |          15.19 |          10.90 |           9.26 |            - |            - |                - |                - |
| UR3D [257]            | Camera | Monocular      | 2020 |                   - |          15.58 |           8.61 |           6.00 |            - |            - |                - |                - |
| D4LCN [60]            | Camera | Monocular      | 2020 |                 200 |          16.65 |          11.72 |           9.51 |            - |            - |                - |                - |
| Ye et al. [345]       | Camera | Monocular      | 2020 |                 400 |          16.77 |          12.72 |           9.17 |            - |            - |                - |                - |
| Kinematic3D [14]      | Camera | Monocular      | 2020 |                 120 |          19.07 |          12.72 |           9.17 |            - |            - |                - |                - |
| CaDDN [237]           | Camera | Monocular      | 2021 |                   - |          19.17 |          13.41 |          11.46 |            - |            - |                - |                - |
| PatchNet [177]        | Camera | Monocular      | 2021 |                 400 |          15.68 |          11.12 |          10.17 |            - |            - |             0.39 |             0.38 |
| MonoDLE [178]         | Camera | Monocular      | 2021 |                   - |          17.23 |          12.26 |          10.29 |            - |            - |                - |                - |
| M3DSSD [173]          | Camera | Monocular      | 2021 |                   - |          17.51 |          11.46 |           8.98 |            - |            - |                - |                - |
| Kumar et al. [121]    | Camera | Monocular      | 2021 |                   - |          18.10 |          12.32 |           9.65 |            - |            - |                - |                - |
| MonoRCNN [258]        | Camera | Monocular      | 2021 |                  70 |          18.36 |          12.65 |          10.03 |            - |            - |                - |                - |
| MonoRUn [31]          | Camera | Monocular      | 2021 |                   - |          19.65 |          12.30 |          10.58 |            - |            - |                - |                - |
| DDMP [288]            | Camera | Monocular      | 2021 |                   - |          19.71 |          12.78 |           9.80 |            - |            - |                - |                - |
| MonoFlex [369]        | Camera | Monocular      | 2021 |                   - |          19.94 |          13.89 |          12.07 |            - |            - |                - |                - |
| GUP Net [172]         | Camera | Monocular      | 2021 |                   - |          20.11 |          14.20 |          11.77 |            - |            - |                - |                - |
| PCT [289]             | Camera | Monocular      | 2021 |                   - |          21.00 |          13.37 |          11.31 |            - |            - |             0.89 |             0.66 |
| MonoEF [384]          | Camera | Monocular      | 2021 |                   - |          21.29 |          13.87 |          11.71 |            - |            - |                - |                - |
| Liu et al. [161]      | Camera | Monocular      | 2021 |                   - |          21.65 |          13.25 |           9.91 |            - |            - |                - |                - |
| DD3D [211]            | Camera | Monocular      | 2021 |                   - |          23.22 |          16.34 |          14.20 |         41.8 |         47.7 |                - |                - |
| FCOS3D [293]          | Camera | Monocular      | 2021 |                   - |              - |              - |              - |         35.8 |         42.8 |                - |                - |
| PGD [294]             | Camera | Monocular      | 2022 |                  28 |              - |              - |              - |         38.6 |         44.8 |                - |                - |
| MonoDTR [107]         | Camera | Monocular      | 2022 |                   - |          21.99 |          15.39 |          12.73 |            - |            - |                - |                - |
| 3DOP [38]             | Camera | Stereo         | 2015 |                   - |              - |              - |              - |            - |            - |                - |                - |
| TLNet [234]           | Camera | Stereo         | 2019 |                   - |           7.64 |           4.37 |           3.74 |            - |            - |                - |                - |
| Stereo R-CNN [134]    | Camera | Stereo         | 2019 |                 420 |          47.58 |          30.23 |          23.72 |            - |            - |                - |                - |
| Pseudo-LiDAR [299]    | Camera | Stereo         | 2019 |                   - |          54.53 |          34.05 |          28.25 |            - |            - |                - |                - |
| IDA-3D [216]          | Camera | Stereo         | 2020 |                   - |              - |              - |              - |            - |            - |                - |                - |
| OC-Stereo [223]       | Camera | Stereo         | 2020 |                 350 |          55.15 |          37.60 |          30.25 |            - |            - |                - |                - |
| ZoomNet [331]         | Camera | Stereo         | 2020 |                 300 |          55.98 |          38.64 |          30.97 |            - |            - |                - |                - |
| Disp R-CNN [267]      | Camera | Stereo         | 2020 |                 420 |          58.53 |          37.91 |          31.93 |            - |            - |                - |                - |
| P-LiDAR++ [354]       | Camera | Stereo         | 2020 |                 500 |          61.11 |          42.43 |          36.99 |            - |            - |                - |                - |
| Qian et al. [231]     | Camera | Stereo         | 2020 |                 400 |           64.8 |           43.9 |           38.1 |            - |            - |                - |                - |
| DSGN [46]             | Camera | Stereo         | 2020 |                 670 |          73.50 |          52.18 |          45.14 |            - |            - |                - |                - |
| CG-Stereo [128]       | Camera | Stereo         | 2020 |                   - |          74.39 |          53.58 |          46.50 |            - |            - |                - |                - |
| CDN [80]              | Camera | Stereo         | 2020 |                 600 |          74.52 |          54.22 |          46.36 |            - |            - |                - |                - |
| PLUMENet [304]        | Camera | Stereo         | 2021 |                 150 |        82.97\* |        66.27\* |        56.70\* |            - |            - |                - |                - |
| LIGA-Stereo [89]      | Camera | Stereo         | 2021 |                 350 |          81.39 |          64.66 |          57.22 |            - |            - |                - |                - |
| Rubino et al. [244]   | Camera | Multi-View     | 2017 |                   - |              - |              - |              - |            - |            - |                - |                - |
| ImVoxelNet [245]      | Camera | Multi-View     | 2021 |                 400 |          17.15 |          10.97 |           9.15 |            - |            - |                - |                - |
| DETR3D [305]          | Camera | Multi-View     | 2021 |                   - |              - |              - |              - |         41.2 |         47.9 |                - |                - |
| PETR [162]            | Camera | Multi-View     | 2022 |                   - |              - |              - |              - |         44.5 |         50.4 |                - |                - |
| BEVDet [106]          | Camera | Multi-View     | 2022 |                   - |              - |              - |              - |         42.2 |         52.9 |                - |                - |
| BEVerse [371]         | Camera | Multi-View     | 2022 |                   - |              - |              - |              - |         39.3 |         53.1 |                - |                - |
| BEVFormer [145]       | Camera | Multi-View     | 2022 |                   - |              - |              - |              - |         48.1 |         56.9 |                - |                - |
| BEVDepth [140]        | Camera | Multi-View     | 2022 |                   - |              - |              - |              - |         52.0 |         60.9 |                - |                - |
| BEVStereo [138]       | Camera | Multi-View     | 2022 |                   - |              - |              - |              - |         52.5 |         61.0 |                - |                - |
| SOLOFusion [212]      | Camera | Multi-View     | 2022 |                   - |              - |              - |              - |         54.0 |         61.9 |                - |                - |
| F-PointNet [226]      | Fusion | Early          | 2018 |                   - |          81.20 |          70.39 |          62.19 |            - |            - |                - |                - |
| RoarNet [259]         | Fusion | Early          | 2019 |                 100 |          83.95 |          75.79 |          67.88 |            - |            - |                - |                - |
| F-ConvNet [306]       | Fusion | Early          | 2019 |                   - |          85.88 |          76.51 |          68.08 |            - |            - |                - |                - |
| PointPainting [281]   | Fusion | Early          | 2020 |                   - |          82.11 |          71.70 |          67.08 |         46.4 |         58.1 |                - |                - |
| FusionPainting [330]  | Fusion | Early          | 2021 |                   - |              - |              - |              - |         66.5 |         70.7 |                - |                - |
| PointAugmenting [282] | Fusion | Early          | 2021 |                 542 |              - |              - |              - |         66.8 |         71.0 |            67.41 |            62.70 |
| MVP [351]             | Fusion | Early          | 2021 |                   - |              - |              - |              - |         66.4 |         70.5 |                - |                - |
| MV3D [41]             | Fusion | Intermediate   | 2017 |                 240 |          71.09 |          62.35 |          55.12 |            - |            - |                - |                - |
| PointFusion [327]     | Fusion | Intermediate   | 2018 |                   - |              - |              - |              - |            - |            - |                - |                - |
| AVOD [117]            | Fusion | Intermediate   | 2018 |                 100 |          81.94 |          71.88 |          66.38 |            - |            - |                - |                - |

Table 18: A comprehensive performance analysis of all branches of 3D object detection methods across different datasets. (Continued)

| Method           | Sensor | Representation | Year | Inference Time (ms) | KITTI Car Easy | KITTI Car Mod. | KITTI Car Hard | nuScenes mAP | nuScenes NDS | Waymo Vehicle L1 | Waymo Vehicle L2 |
| ---------------- | ------ | -------------- | ---: | ------------------: | -------------: | -------------: | -------------: | -----------: | -----------: | ---------------: | ---------------: |
| ContFuse [147]   | Fusion | Intermediate   | 2018 |                  60 |          82.54 |          66.22 |          64.04 |            - |            - |                - |                - |
| MVX-Net [264]    | Fusion | Intermediate   | 2019 |                   - |           83.2 |           72.7 |           65.2 |            - |            - |                - |                - |
| MMF [148]        | Fusion | Intermediate   | 2019 |                  80 |          86.81 |          76.75 |          68.41 |            - |            - |                - |                - |
| 3D-CVF [353]     | Fusion | Intermediate   | 2020 |                  75 |          89.20 |          80.05 |          73.11 |         52.7 |         62.3 |                - |                - |
| EPNet [109]      | Fusion | Intermediate   | 2020 |                   - |          89.81 |          79.28 |          74.59 |            - |            - |                - |                - |
| TransFusion [6]  | Fusion | Intermediate   | 2022 |                   - |              - |              - |              - |         68.9 |         71.7 |                - |                - |
| BEVFusion [150]  | Fusion | Intermediate   | 2022 |                   - |              - |              - |              - |         69.2 |         71.8 |                - |                - |
| UVTR [139]       | Fusion | Intermediate   | 2022 |                   - |              - |              - |              - |         67.1 |         71.1 |                - |                - |
| CLOCs [209]      | Fusion | Late           | 2020 |                 150 |          88.94 |          80.67 |          77.15 |            - |            - |                - |                - |
| Fast-CLOCs [210] | Fusion | Late           | 2022 |                 125 |          89.11 |          80.34 |          76.98 |         63.1 |         68.7 |                - |                - |

## References

[1] H. Abu Alhaija, S. K. Mustikovela, L. Mescheder, A. Geiger, and C. Rother, "Augmented reality meets computer vision: Efficient data generation for urban driving scenes," IJCV, 2018.

[2] H. H. Aghdam, E. J. Heravi, S. S. Demilew, and R. Laganiere, "Rad: Realtime and accurate 3d object detection on embedded systems," in CVPR, 2021.

[3] W. Ali, S. Abdelkarim, M. Zidan, M. Zahran, A. El Sallab, "Yolo3d: End-to-end real-time 3d oriented object bounding box detection from lidar point cloud," in ECCVW, 2018.

[4] A. Amini, I. Gilitschenski, J. Phillips, J. Moseyko, R. Banerjee, S. Karaman, and D. Rus, "Learning robust control policies for end-to-end autonomous driving from data-driven simulation," IEEE RA-L, 2020.

[5] E. Arnold, O. Y. Al-Jarrah, M. Dianati, S. Fallah, D. Oxtoby, and A. Mouzakitis, "A survey on 3d object detection methods for autonomous driving applications," IEEE T-ITS, 2019.

[6] X. Bai, Z. Hu, X. Zhu, Q. Huang, Y. Chen, H. Fu, and C.-L. Tai, "Transfusion: Robust lidar-camera fusion for 3d object detection with transformers," in CVPR, 2022.

[7] W. Bao, B. Xu, and Z. Chen, "Monofenet: Monocular 3d object detection with feature enhancement networks," IEEE T-IP, 2019.

[8] A. Barrera, C. Guindel, J. Beltran, and F. Garcia, "Birdnet+: End-to-end 3d object detection in lidar bird's eye view," in ITSC, 2020.

[9] D. Beker, H. Kato, M. A. Morariu, T. Ando, T. Matsuoka, W. Kehl, and A. Gaidon, "Monocular differentiable rendering for self-supervised 3d object detection," in ECCV, 2020.

[10] J. Beltran, C. Guindel, F. M. Moreno, D. Cruzado, F. Garcia, and A. De La Escalera, "Birdnet: a 3d object detection framework from lidar information," in ITSC, 2018.

[11] A. Bewley, P. Sun, T. Mensink, D. Anguelov, and C. Sminchisescu, "Range conditioned dilated convolutions for scale invariant 3d object detection," arXiv preprint arXiv:200509927, 2020.

[12] M. Bojarski, D. Del Testa, D. Dworakowski, B. Firner, B. Flepp, P. Goyal, L. D. Jackel, M. Monfort, U. Muller, J. Zhang, et al., "End to end learning for self-driving cars," arXiv preprint arXiv:160407316, 2016.

[13] G. Brazil and X. Liu, "M3d-rpn: Monocular 3d region proposal network for object detection," in ICCV, 2019.

[14] G. Brazil, G. Pons-Moll, X. Liu, and B. Schiele, "Kinematic 3d object detection in monocular video," in ECCV, 2020.

[15] H. Caesar, V. Bankiti, A. H. Lang, S. Vora, V. E. Liong, Q. Xu, A. Krishnan, Y. Pan, G. Baldan, and O. Beijbom, "nuscenes: A multimodal dataset for autonomous driving," in CVPR, 2020.

[16] H. Caesar, J. Kabzan, K. S. Tan, W. K. Fong, E. Wolff, A. Lang, L. Fletcher, O. Beijbom, and S. Omari, "nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles," arXiv preprint arXiv:210611810, 2021.

[17] Y. Cai, B. Li, Z. Jiao, H. Li, X. Zeng, and X. Wang, "Monocular 3d object detection with decoupled structured polygon estimation and height-guided depth estimation," in AAAI, 2020.

[18] B. Caine, R. Roelofs, V. Vasudevan, J. Ngiam, Y. Chai, Z. Chen, and J. Shlens, "Pseudo-labeling for scalable 3d object detection," arXiv preprint arXiv:210302093, 2021.

[19] Y. Cao, C. Xiao, B. Cyr, Y. Zhou, W. Park, S. Rampazzi, Q. A. Chen, K. Fu, and Z. M. Mao, "Adversarial sensor attack on lidar-based perception in autonomous driving," in ACM SIGSAC, 2019.

[20] Y. Cao, N. Wang, C. Xiao, D. Yang, J. Fang, R. Yang, Q. A. Chen, M. Liu, and B. Li, "Invisible for both camera and lidar: Security of multi-sensor fusion based perception in autonomous driving under physical-world attacks," in IEEE Symposium on Security and Privacy, 2021.

[21] N. Carion, F. Massa, G. Synnaeve, N. Usunier, A. Kirillov, and S. Zagoruyko, "End-to-end object detection with transformers," in ECCV, 2020.

[22] S. Casas, W. Luo, and R. Urtasun, "Intentnet: Learning to predict intention from raw sensor data," in CoRL, 2018.

[23] S. Casas, A. Sadat, and R. Urtasun, "Mp3: A unified model to map, perceive, predict and plan," in CVPR, 2021.

[24] J. Cen, P. Yun, J. Cai, M. Y. Wang, and M. Liu, "Open-set 3d object detection," in 3DV, 2021.

[25] F. Chabot, M. Chaouch, J. Rabarisoa, C. Teuliere, and T. Chateau, "Deep manta: A coarse-to-fine many-task network for joint 2d and 3d vehicle analysis from monocular image," in CVPR, 2017.

[26] S. Chadwick, W. Maddern, and P. Newman, "Distant vehicle detection using radar and vision," in ICRA, 2019.

[27] Y. Chai, P. Sun, J. Ngiam, W. Wang, B. Caine, V. Vasudevan, X. Zhang, and D. Anguelov, "To the point: Efficient 3d object detection in the range image with graph convolution kernels," in CVPR, 2021.

[28] J. Chang and G. Wetzstein, "Deep optics for monocular depth estimation and 3d object detection," in ICCV, 2019.

[29] J.-R. Chang and Y.-S. Chen, "Pyramid stereo matching network," in CVPR, 2018.

[30] M.-F. Chang, J. Lambert, P. Sangkloy, J. Singh, S. Bak, A. Hartnett, D. Wang, P. Carr, S. Lucey, D. Ramanan, et al., "Argoverse: 3d tracking and forecasting with rich maps," in CVPR, 2019.

[31] H. Chen, Y. Huang, W. Tian, Z. Gao, and L. Xiong, "Monorun: Monocular 3d object detection by reconstruction and uncertainty propagation," in CVPR, 2021.

[32] L. Chen, J. Sun, Y. Xie, S. Zhang, Q. Shuai, Q. Jiang, G. Zhang, H. Bao, and X. Zhou, "Shape prior guided instance disparity estimation for 3d object detection," IEEE T-PAMI, 2021.

[33] Q. Chen, X. Ma, S. Tang, J. Guo, Q. Yang, and S. Fu, "F-cooper: Feature based cooperative perception for autonomous vehicle edge computing system using 3d point clouds," in ACM/IEEE Symposium on Edge Computing, 2019.

[34] Q. Chen, S. Tang, Q. Yang, and S. Fu, "Cooper: Cooperative perception for connected autonomous vehicles based on 3d point clouds," in ICDCS, 2019.

[35] Q. Chen, L. Sun, E. Cheung, and A. L. Yuille, "Every view counts: Cross-view consistency in 3d object detection with hybrid-cylindrical-spherical voxelization," NeurIPS, 2020.

[36] Q. Chen, L. Sun, Z. Wang, K. Jia, and A. Yuille, "Object as hotspots: An anchor-free 3d object detection approach via firing of hotspots," in ECCV, 2020.

[37] Q. Chen, S. Vora, and O. Beijbom, "Polarstream: Streaming lidar object detection and segmentation with polar pillars," arXiv preprint arXiv:210607545, 2021.

[38] X. Chen, K. Kundu, Y. Zhu, A. G. Berneshawi, H. Ma, S. Fidler, and R. Urtasun, "3d object proposals for accurate object class detection," NeurIPS, 2015.

[39] X. Chen, K. Kundu, Z. Zhang, H. Ma, S. Fidler, and R. Urtasun, "Monocular 3d object detection for autonomous driving," in CVPR, 2016.

[40] X. Chen, K. Kundu, Y. Zhu, H. Ma, S. Fidler, and R. Urtasun, "3d object proposals using stereo imagery for accurate object class detection," IEEE T-PAMI, 2017.

[41] X. Chen, H. Ma, J. Wan, B. Li, and T. Xia, "Multi-view 3d object detection network for autonomous driving," in CVPR, 2017.

[42] X. Chen, H. Fan, R. Girshick, and K. He, "Improved baselines with momentum contrastive learning," arXiv preprint arXiv:200304297, 2020.

[43] X. Chen, T. Zhang, Y. Wang, Y. Wang, and H. Zhao, "Futr3d: A unified sensor fusion framework for 3d detection," arXiv preprint arXiv:220310642, 2022.

[44] Y. Chen, S. Liu, X. Shen, and J. Jia, "Fast point r-cnn," in ICCV, 2019.

[45] Y. Chen, H. Li, R. Gao, and D. Zhao, "Boost 3-d object detection via point clouds segmentation and fused 3-d giou loss," IEEE T-NNLS, 2020.

[46] Y. Chen, S. Liu, X. Shen, and J. Jia, "Dsgn: Deep stereo geometry network for 3d object detection," in CVPR, 2020.

[47] Y. Chen, L. Tai, K. Sun, and M. Li, "Monopair: Monocular 3d object detection using pairwise spatial relationships," in CVPR, 2020.

[48] Y. Chen, F. Rong, S. Duggal, S. Wang, X. Yan, S. Manivasagam, S. Xue, E. Yumer, and R. Urtasun, "Geosim: Realistic video simulation via geometry-aware composition for self-driving," in CVPR, 2021.

[49] Y. Chen, Y. Li, X. Zhang, J. Sun, and J. Jia, "Focal sparse convolutional networks for 3d object detection," in CVPR, 2022.

[50] Z. Chen, Z. Li, S. Zhang, L. Fang, Q. Jiang, F. Zhao, B. Zhou, and H. Zhao, "Autolang: Pixel-instance feature aggregation for multi-modal 3d object detection," in IJCAI, 2022.

[51] Y. Choi, N. Kim, S. Hwang, K. Park, J. S. Yoon, K. An, and I. S. Kweon, "Kaist multi-spectral day/night data set for autonomous and assisted driving," T-ITS, 2018.

[52] F. Codevilla, M. Müller, A. López, V. Koltun, and A. Dosovitskiy, "End-to-end driving via conditional imitation learning," in ICRA, 2018.

[53] A. Cui, S. Casas, A. Sadat, R. Liao, and R. Urtasun, "Lookout: Diverse multi-future prediction and planning for self-driving," in ICCV, 2021.

[54] A. Dai, A. X. Chang, M. Savva, M. Halber, T. Funkhouser, and M. Nießner, "Scannet: Richly-annotated 3d reconstructions of indoor scenes," in CVPR, 2017.

[55] R. DeBortoli, L. Fuxin, A. Kapoor, and G. A. Hollinger, "Adversarial training on point clouds for sim-to-real 3d object detection," IEEE RA-L, 2021.

[56] B. Deng, C. R. Qi, M. Najibi, T. Funkhouser, Y. Zhou, and D. Anguelov, "Revisiting 3d object detection from an egocentric perspective," NeurIPS, 2021.

[57] J. Deng, S. Shi, P. Li, W. Zhou, Y. Zhang, and H. Li, "Voxel r-cnn: Towards high performance voxel-based 3d object detection," in AAAI, 2021.

[58] J. Deng, W. Zhou, Y. Zhang, and H. Li, "From multi-view to hollow-3d: Hallucinated hollow-3d r-cnn for 3d object detection," IEEE TCSVT, 2021.

[59] S. Deng, Z. Liang, L. Sun, and K. Jia, "Vista: Boosting 3d object detection via dual cross-view spatial attention," in CVPR, 2022.

[60] M. Ding, Y. Huo, H. Yi, Z. Wang, J. Shi, Z. Lu, and P. Luo, "Learning depth-guided convolutions for monocular 3d object detection," in CVPRW, 2020.

[61] S. Doll, R. Schulz, L. Schneider, V. Benzin, M. Enzweiler, and H. P. Lensch, "Spatialdetr: Robust scalable transformer-based 3d object detection from multi-view camera images with global cross-sensor attention," in ECCV, 2022.

[62] A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, and V. Koltun, "Carla: An open urban driving simulator," in CoRL, 2017.

[63] A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly, et al., "An image is worth 16x16 words: Transformers for image recognition at scale," in ICLR, 2021.

[64] J. Dou, J. Xue, and J. Fang, "Seg-voxelnet for 3d vehicle detection from rgb and lidar data," in ICRA, 2019.

[65] L. Du, X. Ye, X. Tan, J. Feng, Z. Xu, E. Ding, and S. Wen, "Associate-3ddet: Perceptual-to-conceptual association for 3d point cloud object detection," in CVPR, 2020.

[66] L. Du, X. Ye, X. Tan, E. Johns, B. Chen, E. Ding, X. Xue, and J. Feng, "Ago-net: Association-guided 3d point cloud object detection network," IEEE T-PAMI, 2021.

[67] X. Du, M. H. Ang, S. Karaman, and D. Rus, "A general pipeline for 3d detection of vehicles," in ICRA, 2018.

[68] M. Engelcke, D. Rao, D. Z. Wang, C. H. Tong, and I. Posner, "Vote3deep: Fast object detection in 3d point clouds using efficient convolutional neural networks," in ICRA, 2017.

[69] L. Fan, X. Xiong, F. Wang, N. Wang, and Z. Zhang, "Rangedet: In defense of range view for lidar-based 3d object detection," in ICCV, 2021.

[70] L. Fan, Z. Pang, T. Zhang, Y.-X. Wang, H. Zhao, F. Wang, N. Wang, and Z. Zhang, "Embracing single stride 3d object detector with sparse transformer," in CVPR, 2022.

[71] J. Fang, D. Zhou, F. Yan, T. Zhao, F. Zhang, Y. Ma, L. Wang, and R. Yang, "Augmented lidar simulator for autonomous driving," IEEE RA-L, 2020.

[72] J. Fang, D. Zhou, X. Song, and L. Zhang, "Mapfusion: A general framework for 3d object detection with hdmap," in IROS, 2021.

[73] J. Fang, X. Zuo, D. Zhou, S. Jin, S. Wang, and L. Zhang, "Lidar-aug: A general rendering-based augmentation framework for 3d object detection," in CVPR, 2021.

[74] M. Feng, S. Z. Gilani, Y. Wang, L. Zhang, and A. Mian, "Relation graph network for 3d object detection in point clouds," IEEE T-IP, 2020.

[75] D. Fernandes, A. Silva, R. Nevoa, C. Simoes, D. Gonzalez, M. Guevara, P. Novais, J. Monteiro, and P. Melo-Pinto, "Point-cloud based 3d object detection and classification methods for self-driving applications: A survey and taxonomy," Information Fusion, 2021.

[76] D. Frossard, S. Da Suo, S. Casas, J. Tu, and R. Urtasun, "Strobe: Streaming object detection from lidar packets," in CoRL, 2021.

[77] C. Fruhwirth-Reisinger, M. Opitz, H. Possegger, and H. Bischof, "Fast3d: Flow-aware self-training for 3d object detectors," in BMVC, 2021.

[78] H. Fu, M. Gong, C. Wang, K. Batmanghelich, and D. Tao, "Deep ordinal regression network for monocular depth estimation," in CVPR, 2018.

[79] N. Gahlert, N. Jourdan, M. Cordts, U. Franke, and J. Denzler, "Cityscapes 3d: Dataset and benchmark for 9 dof vehicle detection," arXiv preprint arXiv:200607864, 2020.

[80] D. Garg, Y. Wang, B. Hariharan, M. Campbell, K. Q. Weinberger, and W.-L. Chao, "Wasserstein distances for stereo disparity estimation," NeurIPS, 2020.

[81] R. Ge, Z. Ding, Y. Hu, Y. Wang, S. Chen, L. Huang, and Y. Li, "Afdet: Anchor free one stage 3d object detection," arXiv preprint arXiv:200612671, 2020.

[82] A. Geiger, P. Lenz, and R. Urtasun, "Are we ready for autonomous driving? the kitti vision benchmark suite," in CVPR, 2012.

[83] A. Geiger, P. Lenz, C. Stiller, and R. Urtasun, "Vision meets robotics: The kitti dataset," IJRR, 2013.

[84] J. Geyer, Y. Kassahun, M. Mahmudi, X. Ricou, R. Durgesh, A. S. Chung, L. Hauswald, V. H. Pham, M. Muhlegg, S. Dorn, et al., "A2d2: Audi autonomous driving dataset," arXiv preprint arXiv:200406320, 2020.

[85] C. Godard, O. Mac Aodha, and G. J. Brostow, "Unsupervised monocular depth estimation with left-right consistency," in CVPR, 2017.

[86] B. Graham, M. Engelcke, and L. Van Der Maaten, "3d semantic segmentation with submanifold sparse convolutional networks," in CVPR, 2018.

[87] Q. Gu, Q. Zhou, M. Xu, Z. Feng, G. Cheng, X. Lu, J. Shi, and L. Ma, "Pit: Position-invariant transform for cross-fov domain adaptation," in ICCV, 2021.

[88] T. Guan, J. Wang, S. Lan, R. Chandra, Z. Wu, L. Davis, and D. Manocha, "M3detr: Multi-representation, multi-scale, mutual-relation 3d object detection with transformers," in WACV, 2022.

[89] X. Guo, S. Shi, X. Wang, and H. Li, "Liga-stereo: Learning lidar geometry aware representations for stereo-based 3d detector," in ICCV, 2021.

[90] Y. Guo, H. Wang, Q. Hu, H. Liu, L. Liu, and M. Bennamoun, "Deep learning for 3d point clouds: A survey," IEEE T-PAMI, 2020.

[91] M. Hahner, C. Sakaridis, D. Dai, and L. Van Gool, "Fog simulation on real lidar point clouds for 3d object detection in adverse weather," in ICCV, 2021.

[92] W. Han, Z. Zhang, B. Caine, B. Yang, C. Sprunk, O. Alsharif, J. Ngiam, V. Vasudevan, J. Shlens, and Z. Chen, "Streaming object detection for 3-d point clouds," in ECCV, 2020.

[93] R. Hartley and A. Zisserman, "Multiple view geometry in computer vision," Cambridge university press, 2003.

[94] C. He, H. Zeng, J. Huang, X.-S. Hua, and L. Zhang, "Structure aware single-stage 3d object detection from point cloud," in CVPR, 2020.

[95] K. He, X. Zhang, S. Ren, and J. Sun, "Deep residual learning for image recognition," in CVPR, 2016.

[96] K. He, H. Fan, Y. Wu, S. Xie, and R. Girshick, "Momentum contrast for unsupervised visual representation learning," in CVPR, 2020.

[97] Q. He, Z. Wang, H. Zeng, Y. Zeng, S. Liu, and B. Zeng, "Svganet: Sparse voxel-graph attention network for 3d object detection from point clouds," arXiv preprint arXiv:200604043, 2020.

[98] T. He and S. Soatto, "Mono3d++: Monocular 3d vehicle detection with two-scale 3d hypotheses and task priors," in AAAI, 2019.

[99] J. Heylen, M. De Wolf, B. Dawange, M. Proesmans, L. Van Gool, W. Abbeloos, H. Abdelkawy, and D. O. Reino, "Monoclinis: Camera independent monocular 3d object detection using instance segmentation," in ICCV, 2021.

[100] H.-N. Hu, Q.-Z. Cai, D. Wang, J. Lin, M. Sun, P. Krahenbuhl, T. Darrell, and F. Yu, "Joint monocular 3d vehicle detection and tracking," in ICCV, 2019.

[101] J. S. Hu, T. Kuai, and S. L. Waslander, "Point density-aware voxels for lidar 3d object detection," in CVPR, 2022.

[102] P. Hu, J. Ziglar, D. Held, and D. Ramanan, "What you see is what you get: Exploiting visibility for 3d object detection," in CVPR, 2020.

[103] Y. Hu, Z. Ding, R. Ge, W. Shao, L. Huang, K. Li, and Q. Liu, "Afdetv2: Rethinking the necessity of the second stage for object detection from point clouds," arXiv preprint arXiv:211209205, 2021.

[104] B. Huang, Y. Li, E. Xie, F. Liang, L. Wang, M. Shen, F. Liu, T. Wang, P. Luo, and J. Shao, "Fast-bev: Towards real-time on-vehicle bird's-eye view perception," in NeurIPS, 2022.

[105] J. Huang and G. Huang, "Bevdet4d: Exploit temporal cues in multi-camera 3d object detection," arXiv preprint arXiv:220317054, 2022.

[106] J. Huang, G. Huang, D. Zhu, and D. Du, "Bevdet: High-performance multi-camera 3d object detection in bird-eye-view," arXiv preprint arXiv:211211790, 2021.

[107] K.-C. Huang, T.-H. Wu, H.-T. Su, and W. H. Hsu, "Monodtr: Monocular 3d object detection with depth-aware transformer," in CVPR, 2022.

[108] R. Huang, W. Zhang, A. Kundu, C. Pantofaru, D. A. Ross, T. Funkhouser, and A. Fathi, "An lstm approach to temporal 3d object detection in lidar point clouds," in ECCV, 2020.

[109] T. Huang, Z. Liu, X. Chen, and X. Bai, "Epnet: Enhancing point features with image semantics for 3d object detection," in ECCV, 2020.

[110] X. Huang, P. Wang, X. Cheng, D. Zhou, Q. Geng, and R. Yang, "The apolloscape open dataset for autonomous driving and its application," IEEE T-PAMI, 2019.

[111] B. Jiang, S. Chen, X. Wang, B. Liao, T. Cheng, J. Chen, H. Zhou, Q. Zhang, W. Liu, and C. Huang, "Perceive, interact, predict: Learning dynamic and static clues for end-to-end motion prediction," arXiv preprint arXiv:221202181, 2022.

[112] E. Jorgensen, C. Zach, and F. Kahl, "Monocular 3d object detection and box fitting trained end-to-end using intersection-over-union loss," arXiv preprint arXiv:190608070, 2019.

[113] A. Kendall, J. Hawke, D. Janz, P. Mazur, D. Reda, J.-M. Allen, V.-D. Lam, A. Bewley, and A. Shah, "Learning to drive in a day," in ICRA, 2019.

[114] R. Kesten, M. Usman, J. Houston, T. Pandya, K. Nadhamuni, A. Ferreira, M. Yuan, B. Low, A. Jain, P. Ondruska, S. Omari, S. Shah, A. Kulkarni, A. Kazakova, C. Tao, L. Platinsky, W. Jiang, and V. Shet, "Lyft level 5 av dataset 2019," https://level5.lyft.com/dataset/, 2019.

[115] S. W. Kim, J. Philion, A. Torralba, and S. Fidler, "Drivegan: Towards a controllable high-quality neural simulation," in CVPR, 2021.

[116] H. Konighof, N. O. Salscheider, and C. Stiller, "Realtime 3d object detection for automated driving using stereo vision and semantic information," in ITSC, 2019.

[117] J. Ku, M. Mozifian, J. Lee, A. Harakeh, and S. L. Waslander, "Joint 3d proposal generation and object detection from view aggregation," in IROS, 2018.

[118] J. Ku, A. D. Pon, and S. L. Waslander, "Monocular 3d object detection leveraging accurate proposals and shape reconstruction," in CVPR, 2019.

[119] H. Kuang, B. Wang, J. An, M. Zhang, and Z. Zhang, "Voxel-fpn: Multi-scale voxel feature aggregation for 3d object detection from lidar point clouds," Sensors, 2020.

[120] H. W. Kuhn, "The hungarian method for the assignment problem," Naval research logistics quarterly, 1955.

[121] A. Kumar, G. Brazil, and X. Liu, "Groomed-nms: Grouped mathematically differentiable nms for monocular 3d object detection," in CVPR, 2021.

[122] A. Kundu, Y. Li, and J. M. Rehg, "3d-rcnn: Instance-level 3d object reconstruction via render-and-compare," in CVPR, 2018.

[123] A. Laddha, S. Gautam, G. P. Meyer, C. Vallespi-Gonzalez, and C. K. Wellington, "Rv-fusenet: Range view based fusion of time-series lidar data for joint 3d object detection and motion forecasting," in IROS, 2020.

[124] A. H. Lang, S. Vora, H. Caesar, L. Zhou, J. Yang, and O. Beijbom, "Pointpillars: Fast encoders for object detection from point clouds," in CVPR, 2019.

[125] B. Li, "3d fully convolutional network for vehicle detection in point cloud," in IROS, 2017.

[126] B. Li, T. Zhang, and T. Xia, "Vehicle detection from 3d lidar using fully convolutional network," arXiv preprint arXiv:160807916, 2016.

[127] B. Li, W. Ouyang, L. Sheng, X. Zeng, and X. Wang, "Gs3d: An efficient 3d object detection framework for autonomous driving," in CVPR, 2019.

[128] C. Li, J. Ku, and S. L. Waslander, "Confidence guided stereo 3d object detection with split depth estimation," in IROS, 2020.

[129] F. Li, W. Jin, C. Fan, L. Zou, Q. Chen, X. Li, H. Jiang, and Y. Liu, "Psanet: Pyramid splitting and aggregation network for 3d object detection in point cloud," Sensors, 2021.

[130] J. Li, H. Dai, L. Shao, and Y. Ding, "Anchor-free 3d single stage detector with mask-guided attention for point cloud," in ACM Multimedia, 2021.

[131] J. Li, H. Dai, L. Shao, and Y. Ding, "From voxel to point: Iou-guided 3d object detection for point cloud with voxel-to-point decoder," in ACM Multimedia, 2021.

[132] L. L. Li, B. Yang, M. Liang, W. Zeng, M. Ren, S. Segal, and R. Urtasun, "End-to-end contextual perception and prediction with interaction transformer," in IROS, 2020.

[133] P. Li and H. Zhao, "Monocular 3d detection with geometric constraint embedding and semi-supervised training," IEEE RA-L, 2021.

[134] P. Li, X. Chen, and S. Shen, "Stereo r-cnn based 3d object detection for autonomous driving," in CVPR, 2019.

[135] P. Li, H. Zhao, P. Liu, and F. Cao, "Rtm3d: Real-time monocular 3d detection from object keypoints for autonomous driving," in ECCV, 2020.

[136] Y. Li, S. Ren, P. Wu, S. Chen, C. Feng, and W. Zhang, "Learning distilled collaboration graph for multi-agent perception," NeurIPS, 2021.

[137] Y. Li, C. Wen, F. Juefei-Xu, and C. Feng, "Fooling lidar perception via adversarial trajectory perturbation," in ICCV, 2021.

[138] Y. Li, H. Bao, Z. Ge, J. Yang, J. Sun, and Z. Li, "Bevstereo: Enhancing depth estimation in multi-view 3d object detection with dynamic temporal stereo," arXiv preprint arXiv:220910248, 2022.

[139] Y. Li, Y. Chen, X. Qi, Z. Li, J. Sun, and J. Jia, "Unifying voxel-based representation with transformer for 3d object detection," in NeurIPS, 2022.

[140] Y. Li, Z. Ge, G. Yu, J. Yang, Z. Wang, Y. Shi, J. Sun, and Z. Li, "Bevdepth: Acquisition of reliable depth for multi-view 3d object detection," arXiv preprint arXiv:220610092, 2022.

[141] Y. Li, X. Qi, Y. Chen, L. Wang, Z. Li, J. Sun, and J. Jia, "Voxel field fusion for 3d object detection," in CVPR, 2022.

[142] Y. Li, A. W. Yu, T. Meng, B. Caine, J. Ngiam, D. Peng, J. Shen, B. Wu, Y. Lu, D. Zhou, et al., "Deepfusion: Lidar-camera deep fusion for multi-modal 3d object detection," in CVPR, 2022.

[143] Z. Li, Z. Chen, A. Li, L. Fang, Q. Jiang, X. Liu, J. Jiang, B. Zhou, and H. Zhao, "Simpu: Simple 2d image and 3d point cloud unsupervised pre-training for spatial-aware visual representations," in AAAI, 2021.

[144] Z. Li, F. Wang, and N. Wang, "Lidar r-cnn: An efficient and universal 3d object detector," in CVPR, 2021.

[145] Z. Li, W. Wang, H. Li, E. Xie, C. Sima, T. Lu, Q. Yu, and J. Dai, "Bevformer: Learning bird's-eye-view representation from multi-camera images via spatiotemporal transformers," in ECCV, 2022.

[146] H. Liang, C. Jiang, D. Feng, X. Chen, H. Xu, X. Liang, W. Zhang, Z. Li, and L. Van Gool, "Exploring geometry-aware contrast and clustering harmonization for self-supervised 3d object detection," in ICCV, 2021.

[147] M. Liang, B. Yang, S. Wang, and R. Urtasun, "Deep continuous fusion for multi-sensor 3d object detection," in ECCV, 2018.

[148] M. Liang, B. Yang, Y. Chen, R. Hu, and R. Urtasun, "Multi-task multi-sensor fusion for 3d object detection," in CVPR, 2019.

[149] M. Liang, B. Yang, W. Zeng, Y. Chen, R. Hu, S. Casas, and R. Urtasun, "Pnpnet: End-to-end perception and prediction with tracking in the loop," in CVPR, 2020.

[150] T. Liang, H. Xie, K. Yu, Z. Xia, Z. Lin, Y. Wang, T. Tang, B. Wang, and Z. Tang, "Bevfusion: A simple and robust lidar-camera fusion framework," in NeurIPS, 2022.

[151] W. Liang, P. Xu, L. Guo, H. Bai, Y. Zhou, and F. Chen, "A survey of 3d object detection," Multimedia Tools and Applications, 2021.

[152] Z. Liang, M. Zhang, Z. Zhang, X. Zhao, and S. Pu, "Rangercnn: Towards fast and accurate 3d object detection with range image representation," arXiv preprint arXiv:200900206, 2020.

[153] Z. Liang, Z. Zhang, M. Zhang, X. Zhao, and S. Pu, "Rangeioudet: Range image based real-time 3d object detector optimized by intersection over union," in CVPR, 2021.

[154] Y. Liao, J. Xie, and A. Geiger, "Kitti-360: A novel dataset and benchmarks for urban scene understanding in 2d and 3d," arXiv preprint arXiv:210913410, 2021.

[155] T.-Y. Lin, M. Maire, S. Belongie, J. Hays, P. Perona, D. Ramanan, P. Dollar, and C. L. Zitnick, "Microsoft coco: Common objects in context," in ECCV, 2014.

[156] T.-Y. Lin, P. Dollar, R. Girshick, K. He, B. Hariharan, and S. Belongie, "Feature pyramid networks for object detection," in CVPR, 2017.

[157] T.-Y. Lin, P. Goyal, R. Girshick, K. He, and P. Dollar, "Focal loss for dense object detection," in ICCV, 2017.

[158] Y. Lin, Z. Zhang, H. Tang, H. Wang, and S. Han, "Pointacc: Efficient point cloud accelerator," in MICRO, 2021.

[159] L. Liu, J. Lu, C. Xu, Q. Tian, and J. Zhou, "Deep fitting degree scoring network for monocular 3d object detection," in CVPR, 2019.

[160] Y. Liu, L. Wang, and M. Liu, "Yolostereo3d: A step back to 2d for efficient stereo 3d detection," in ICRA, 2021.

[161] Y. Liu, Y. Yixuan, and M. Liu, "Ground-aware monocular 3d object detection for autonomous driving," IEEE RA-L, 2021.

[162] Y. Liu, T. Wang, X. Zhang, and J. Sun, "Petr: Position embedding transformation for multi-view 3d object detection," in ECCV, 2022.

[163] Y.-C. Liu, J. Tian, N. Glaser, and Z. Kira, "When2com: Multi-agent perception via communication graph grouping," in CVPR, 2020.

[164] Y.-C. Liu, J. Tian, C.-Y. Ma, N. Glaser, C.-W. Kuo, and Z. Kira, "Who2com: Collaborative perception via learnable handshake communication," in ICRA, 2020.

[165] Z. Liu, H. Tang, Y. Lin, and S. Han, "Point-voxel cnn for efficient 3d deep learning," NeurIPS, 2019.

[166] Z. Liu, Z. Wu, and R. Toth, "Smoke: Single-stage monocular 3d object detection via keypoint estimation," in CVPRW, 2020.

[167] Z. Liu, X. Zhao, T. Huang, R. Hu, Y. Zhou, and X. Bai, "Tanet: Robust 3d object detection from point clouds with triple attention," in AAAI, 2020.

[168] Z. Liu, Y. Lin, Y. Cao, H. Hu, Y. Wei, Z. Zhang, S. Lin, and B. Guo, "Swin transformer: Hierarchical vision transformer using shifted windows," in ICCV, 2021.

[169] Z. Liu, Z. Zhang, Y. Cao, H. Hu, and X. Tong, "Group-free 3d object detection via transformers," in ICCV, 2021.

[170] Z. Liu, H. Tang, A. Amini, X. Yang, H. Mao, D. Rus, and S. Han, "Bevfusion: Multi-task multi-sensor fusion with unified bird's-eye view representation," arXiv preprint arXiv:220513542, 2022.

[171] J. Long, E. Shelhamer, and T. Darrell, "Fully convolutional networks for semantic segmentation," in CVPR, 2015.

[172] Y. Lu, X. Ma, L. Yang, T. Zhang, Y. Liu, Q. Chu, J. Yan, and W. Ouyang, "Geometry uncertainty projection network for monocular 3d object detection," in ICCV, 2021.

[173] S. Luo, H. Dai, L. Shao, and Y. Ding, "M3dssd: Monocular 3d single stage object detector," in CVPR, 2021.

[174] W. Luo, B. Yang, and R. Urtasun, "Fast and furious: Real time end-to-end 3d detection, tracking and motion forecasting with a single convolutional net," in CVPR, 2018.

[175] Z. Luo, Z. Cai, C. Zhou, G. Zhang, H. Zhao, S. Yi, S. Lu, H. Li, S. Zhang, and Z. Liu, "Unsupervised domain adaptive 3d detection with multi-level consistency," in ICCV, 2021.

[176] X. Ma, Z. Wang, H. Li, P. Zhang, W. Ouyang, and X. Fan, "Accurate monocular 3d object detection via color-embedded 3d reconstruction for autonomous driving," in ICCV, 2019.

[177] X. Ma, S. Liu, Z. Xia, H. Zhang, X. Zeng, and W. Ouyang, "Rethinking pseudo-lidar representation," in ECCV, 2020.

[178] X. Ma, Y. Zhang, D. Xu, D. Zhou, S. Yi, H. Li, and W. Ouyang, "Delving into localization errors for monocular 3d object detection," in CVPR, 2021.

[179] X. Ma, W. Ouyang, A. Simonelli, and E. Ricci, "3d object detection from images for autonomous driving: A survey," arXiv preprint arXiv:220202980, 2022.

[180] Y. Ma, X. Zhu, S. Zhang, R. Yang, W. Wang, and D. Manocha, "Trafficpredict: Trajectory prediction for heterogeneous traffic-agents," in AAAI, 2019.

[181] B. Major, D. Fontijne, A. Ansari, R. Teja Sukhavasi, R. Gowaikar, M. Hamilton, S. Lee, S. Grzechnik, and S. Subramanian, "Vehicle detection with automotive radar using deep learning on range-azimuth-doppler tensors," in ICCVW, 2019.

[182] F. Manhardt, W. Kehl, and A. Gaidon, "Roi-10d: Monocular lifting of 2d detection to 6d pose and metric shape," in CVPR, 2019.

[183] S. Manivasagam, S. Wang, K. Wong, W. Zeng, M. Sazanovich, S. Tan, B. Yang, W.-C. Ma, and R. Urtasun, "Lidarsim: Realistic lidar simulation by leveraging the real world," in CVPR, 2020.

[184] J. Mao, X. Wang, and H. Li, "Interpolated convolutional networks for 3d point cloud understanding," in ICCV, 2019.

[185] J. Mao, M. Niu, H. Bai, X. Liang, H. Xu, and C. Xu, "Pyramid r-cnn: Towards better performance and adaptability for 3d object detection," in ICCV, 2021.

[186] J. Mao, M. Niu, C. Jiang, H. Liang, J. Chen, X. Liang, Y. Li, C. Ye, W. Zhang, Z. Li, et al., "One million scenes for autonomous driving: Once dataset," in NeurIPS, 2021.

[187] J. Mao, Y. Xue, M. Niu, H. Bai, J. Feng, X. Liang, H. Xu, and C. Xu, "Voxel transformer for 3d object detection," in ICCV, 2021.

[188] N. Mayer, E. Ilg, P. Hausser, P. Fischer, D. Cremers, A. Dosovitskiy, and T. Brox, "A large dataset to train convolutional networks for disparity, optical flow, and scene flow estimation," in CVPR, 2016.

[189] Q. Meng, W. Wang, T. Zhou, J. Shen, L. V. Gool, and D. Dai, "Weakly supervised 3d object detection from lidar point cloud," in ECCV, 2020.

[190] Q. Meng, W. Wang, T. Zhou, J. Shen, Y. Jia, and L. Van Gool, "Towards a weakly supervised framework for 3d point cloud object detection and annotation," IEEE T-PAMI, 2021.

[191] G. P. Meyer, J. Charland, D. Hegde, A. Laddha, and C. Vallespi-Gonzalez, "Sensor fusion for joint 3d object detection and semantic segmentation," in CVPRW, 2019.

[192] G. P. Meyer, A. Laddha, E. Kee, C. Vallespi-Gonzalez, and C. K. Wellington, "Lasernet: An efficient probabilistic 3d object detector for autonomous driving," in CVPR, 2019.

[193] G. P. Meyer, J. Charland, S. Pandey, A. Laddha, S. Gautam, C. Vallespi-Gonzalez, and C. K. Wellington, "Laserflow: Efficient and probabilistic object detection and motion forecasting," IEEE RA-L, 2020.

[194] M. Meyer, G. Kuschk, and S. Tomforde, "Graph convolutional networks for 3d object detection on radar data," in ICCV, 2021.

[195] Z. Miao, J. Chen, H. Pan, R. Zhang, K. Liu, P. Hao, J. Zhu, Y. Wang, and X. Zhan, "Pygnet: A bottom-up one-stage 3d object detector with integrated multi-level features," in CVPR, 2021.

[196] I. Misra, R. Girdhar, and A. Joulin, "An end-to-end transformer model for 3d object detection," in ICCV, 2021.

[197] A. Mousavian, D. Anguelov, J. Flynn, and J. Kosecka, "3d bounding box estimation using deep learning and geometry," in CVPR, 2017.

[198] R. Nabati and H. Qi, "Rrpn: Radar region proposal network for object detection in autonomous vehicles," in ICIP, 2019.

[199] R. Nabati and H. Qi, "Centerfusion: Center-based radar and camera fusion for 3d object detection," in WACV, 2021.

[200] A. Naiden, V. Paunescu, G. Kim, B. Jeon, and M. Leordeanu, "Shift r-cnn: Deep monocular 3d object detection with closed-form geometric constraints," in ICIP, 2019.

[201] M. Najibi, G. Lai, A. Kundu, Z. Lu, V. Rathod, T. Funkhouser, C. Pantofaru, D. Ross, L. S. Davis, and A. Fathi, "Dops: Learning to detect 3d objects and predict their 3d shapes," in CVPR, 2020.

[202] K. Nakashima and R. Kurazume, "Learning to drop points for lidar scan synthesis," in IROS, 2021.

[203] J. Ngiam, B. Caine, W. Han, B. Yang, Y. Chai, P. Sun, Y. Zhou, X. Yi, O. Alsharif, P. Nguyen, et al., "Starnet: Targeted computation for object detection in point clouds," arXiv preprint arXiv:190811069, 2019.

[204] J. Noh, S. Lee, and B. Ham, "Hvpr: Hybrid voxel-point representation for single-stage 3d object detection," in CVPR, 2021.

[205] A. Paigwar, O. Erkent, C. Wolf, and C. Laugier, "Attentional pointnet for 3d-object detection in point clouds," in CVPRW, 2019.

[206] A. Paigwar, D. Sierra-Gonzalez, O. Erkent, and C. Laugier, "Frustum-pointpillars: A multi-stage approach for 3d object detection using rgb camera and lidar," in ICCV, 2021.

[207] A. Palffy, E. Pool, S. Baratam, J. F. Kooij, and D. M. Gavrila, "Multiclass road user detection with 3+1 d radar in the view-of-delft dataset," IEEE RA-L, 2022.

[208] X. Pan, Z. Xia, S. Song, L. E. Li, and G. Huang, "3d object detection with pointformer," in CVPR, 2021.

[209] S. Pang, D. Morris, and H. Radha, "Clocs: Camera-lidar object candidates fusion for 3d object detection," in IROS, 2020.

[210] S. Pang, D. Morris, and H. Radha, "Fast-clocs: Fast camera-lidar object candidates fusion for 3d object detection," in WACV, 2022.

[211] D. Park, R. Ambrus, V. Guizilini, J. Li, and A. Gaidon, "Is pseudo-lidar needed for monocular 3d object detection?," in ICCV, 2021.

[212] J. Park, C. Xu, S. Yang, K. Keutzer, K. Kitani, M. Tomizuka, and W. Zhan, "Time will tell: New outlooks and a baseline for temporal multi-view 3d object detection," arXiv preprint arXiv:221002443, 2022.

[213] J. J. Park, P. Florence, J. Straub, R. Newcombe, and S. Lovegrove, "Deepsdf: Learning continuous signed distance functions for shape representation," in CVPR, 2019.

[214] A. Patil, S. Malla, H. Gang, and Y.-T. Chen, "The h3d dataset for full-surround 3d multi-object detection and tracking in crowded urban scenes," in ICRA, 2019.

[215] L. Peng, S. Yan, B. Wu, Z. Yang, X. He, and D. Cai, "Weakm3d: Towards weakly supervised monocular 3d object detection," in ICLR, 2021.

[216] W. Peng, H. Pan, H. Liu, and Y. Sun, "Ida-3d: Instance-depth-aware 3d object detection from stereo vision for autonomous driving," in CVPR, 2020.

[217] X. Peng, X. Zhu, T. Wang, and Y. Ma, "Side: Center-based stereo 3d detector with structure-aware instance depth estimation," in WACV, 2022.

[218] Q.-H. Pham, P. Sevestre, R. S. Pahwa, H. Zhan, C. H. Pang, Y. Chen, A. Mustafa, V. Chandrasekhar, and J. Lin, "A\* 3d dataset: Towards autonomous driving in challenging environments," in ICRA, 2020.

[219] J. Philion and S. Fidler, "Lift, splat, shoot: Encoding images from arbitrary camera rigs by implicitly unprojecting to 3d," in ECCV, 2020.

[220] J. Philion, A. Kar, and S. Fidler, "Learning to evaluate perception models using planner-centric metrics," in CVPR, 2020.

[221] J. Phillips, J. Martinez, I. A. Barsan, S. Casas, A. Sadat, and R. Urtasun, "Deep multi-task learning for joint localization, perception, and prediction," in CVPR, 2021.

[222] A. Piergiovanni, V. Casser, M. S. Ryoo, and A. Angelova, "4d-net for learned multi-modal alignment," in ICCV, 2021.

[223] A. D. Pon, J. Ku, C. Li, and S. L. Waslander, "Object-centric stereo matching for 3d object detection," in ICRA, 2020.

[224] C. R. Qi, H. Su, K. Mo, and L. J. Guibas, "Pointnet: Deep learning on point sets for 3d classification and segmentation," in CVPR, 2017.

[225] C. R. Qi, L. Yi, H. Su, and L. J. Guibas, "Pointnet++ deep hierarchical feature learning on point sets in a metric space," in NeurIPS, 2017.

[226] C. R. Qi, W. Liu, C. Wu, H. Su, and L. J. Guibas, "Frustum pointnets for 3d object detection from rgb-d data," in CVPR, 2018.

[227] C. R. Qi, O. Litany, K. He, and L. J. Guibas, "Deep hough voting for 3d object detection in point clouds," in ICCV, 2019.

[228] C. R. Qi, X. Chen, O. Litany, and L. J. Guibas, "Imvotenet: Boosting 3d object detection in point clouds with image votes," in CVPR, 2020.

[229] C. R. Qi, Y. Zhou, M. Najibi, P. Sun, K. Vo, B. Deng, and D. Anguelov, "Offboard 3d object detection from point cloud sequences," in CVPR, 2021.

[230] K. Qian, S. Zhu, X. Zhang, and L. E. Li, "Robust multimodal vehicle detection in foggy weather using complementary lidar and radar signals," in CVPR, 2021.

[231] R. Qian, D. Garg, Y. Wang, Y. You, S. Belongie, B. Hariharan, M. Campbell, K. Q. Weinberger, and W.-L. Chao, "End-to-end pseudo-lidar for image-based 3d object detection," in CVPR, 2020.

[232] R. Qian, X. Lai, and X. Li, "3d object detection for autonomous driving: A survey," Pattern Recognition, 2021.

[233] Z. Qin, J. Wang, and Y. Lu, "Monogrnet: A geometric reasoning network for monocular 3d object localization," in AAAI, 2019.

[234] Z. Qin, J. Wang, and Y. Lu, "Triangulation learning network: from monocular to stereo 3d object detection," in CVPR, 2019.

[235] Z. Qin, J. Wang, and Y. Lu, "Weakly supervised 3d object detection from point clouds," in ACM Multimedia, 2020.

[236] M. Rapoport-Lavie and D. Raviv, "It's all around you: Range-guided cylindrical network for 3d object detection," in ICCV, 2021.

[237] C. Reading, A. Harakeh, J. Chae, and S. L. Waslander, "Categorical depth distribution network for monocular 3d object detection," in CVPR, 2021.

[238] S. Ren, K. He, R. Girshick, and J. Sun, "Faster r-cnn: Towards real-time object detection with region proposal networks," NeurIPS, 2015.

[239] S. Ren, K. He, R. Girshick, and J. Sun, "Faster r-cnn: Towards real-time object detection with region proposal networks," NeurIPS, 2015.

[240] C. B. Rist, M. Enzweiler, and D. M. Gavrila, "Cross-sensor deep domain adaptation for lidar detection and segmentation," in IV, 2019.

[241] T. Roddick, A. Kendall, and R. Cipolla, "Orthographic feature transform for monocular 3d object detection," in BMVC, 2019.

[242] O. Ronneberger, P. Fischer, and T. Brox, "U-net: Convolutional networks for biomedical image segmentation," in MICCAI, 2015.

[243] G. Ros, L. Sellart, J. Materzynska, D. Vazquez, and A. M. Lopez, "The synthia dataset: A large collection of synthetic images for semantic segmentation of urban scenes," in CVPR, 2016.

[244] C. Rubino, M. Crocco, and A. Del Bue, "3d object localisation from multi-view image detections," IEEE T-PAMI, 2017.

[245] D. Rukhovich, A. Vorontsova, and A. Konushin, "Imoxelnet: Image to voxels projection for monocular and multi-view general-purpose 3d object detection," in WACV, 2022.

[246] A. Sadat, S. Casas, M. Ren, X. Wu, P. Dhawan, and R. Urtasun, "Perceive, predict, and plan: Safe motion planning through interpretable semantic representations," in ECCV, 2020.

[247] K. Saleh, A. Abobakr, M. Attia, J. Iskander, D. Nahavandi, M. Hossny, and S. Nahvandi, "Domain adaptation for vehicle detection from bird's eye view lidar point cloud data," in ICCVW, 2019.

[248] C. Saltori, S. Lathuilière, N. Sebe, E. Ricci, and F. Galasso, "Sfuda 3d: Source-free unsupervised domain adaptation for lidar-based 3d object detection," in 3DV, 2020.

[249] S. Shah, D. Dey, C. Lovett, and A. Kapoor, "Airsim: High-fidelity visual and physical simulation for autonomous vehicles," in Field and service robotics, 2018.

[250] H. Sheng, S. Cai, Y. Liu, B. Deng, J. Huang, X.-S. Hua, and M.-J. Zhao, "Improving 3d object detection with channel-wise transformer," in ICCV, 2021.

[251] G. Shi, R. Li, and C. Ma, "Pillarnet: Real-time and high-performance pillar-based 3d object detection," in ECCV, 2022.

[252] S. Shi, X. Wang, and H. Li, "Pointrcnn: 3d object proposal generation and detection from point cloud," in CVPR, 2019.

[253] S. Shi, C. Guo, L. Jiang, Z. Wang, J. Shi, X. Wang, and H. Li, "Pvrcnn: Point-voxel feature set abstraction for 3d object detection," in CVPR, 2020.

[254] S. Shi, Z. Wang, J. Shi, X. Wang, and H. Li, "From points to parts: 3d object detection from point cloud with part-aware and part-aggregation network," IEEE T-PAMI, 2020.

[255] S. Shi, L. Jiang, J. Deng, Z. Wang, C. Guo, J. Shi, X. Wang, and H. Li, "Pvrcnn++: Point-voxel feature set abstraction with local vector representation for 3d object detection," arXiv preprint arXiv:210200463, 2021.

[256] W. Shi and R. Rajkumar, "Point-gnn: Graph neural network for 3d object detection in a point cloud," in CVPR, 2020.

[257] X. Shi, Z. Chen, and T.-K. Kim, "Distance-normalized unified representation for monocular 3d object detection," in ECCV, 2020.

[258] X. Shi, Q. Ye, X. Chen, C. Chen, Z. Chen, and T.-K. Kim, "Geometry-based distance decomposition for monocular 3d object detection," in ICCV, 2021.

[259] K. Shin, Y. P. Kwon, and M. Tomizuka, "Roarnet: A robust 3d object detection based on region approximation refinement," in IV, 2019.

[260] M. Simon, K. Amende, A. Kraus, J. Honer, T. Samann, H. Kaulbersch, S. Milz, and H. Michael Gross, "Complexer-yolo: Real-time 3d object detection and tracking on semantic point clouds," in CVPRW, 2019.

[261] A. Simonelli, S. R. Bulo, L. Porzi, M. Lopez-Antequera, and P. Kontschieder, "Disentangling monocular 3d object detection," in ICCV, 2019.

[262] A. Simonelli, S. R. Bulo, L. Porzi, E. Ricci, and P. Kontschieder, "Towards generalization across depth for monocular 3d object detection," in ECCV, 2020.

[263] M. Simony, S. Milzy, K. Amendey, and H.-M. Gross, "Complexyolo: An euler-region-proposal for real-time 3d object detection on point clouds," in ECCVW, 2018.

[264] V. A. Sindagi, Y. Zhou, and O. Tuzel, "Mvx-net: Multimodal voxelnet for 3d object detection," in ICRA, 2019.

[265] S. Song, S. P. Lichtenberg, and J. Xiao, "Sun rgb-d: A rgb-d scene understanding benchmark suite," in CVPR, 2015.

[266] J. Sun, Y. Cao, Q. A. Chen, and Z. M. Mao, "Towards robust [LiDAR-based] perception in autonomous driving: General blackbox adversarial sensor attack and countermeasures," in USENIX Security, 2020.

[267] J. Sun, L. Chen, Y. Xie, S. Zhang, Q. Jiang, X. Zhou, and H. Bao, "Disp r-cnn: Stereo 3d object detection via shape prior guided instance disparity estimation," in CVPR, 2020.

[268] P. Sun, H. Kretzschmar, X. Dotiwalla, A. Chouard, V. Patnaik, P. Tsui, J. Guo, Y. Zhou, Y. Chai, B. Caine, et al., "Scalability in perception for autonomous driving: Waymo open dataset," in CVPR, 2020.

[269] P. Sun, W. Wang, Y. Chai, G. Elsayed, A. Bewley, X. Zhang, C. Sminchisescu, and D. Anguelov, "Rsn: Range sparse net for efficient, accurate lidar 3d object detection," in CVPR, 2021.

[270] P. Sun, M. Tan, W. Wang, C. Liu, F. Xia, Z. Leng, and D. Anguelov, "Swformer: Sparse window transformer for 3d object detection in point clouds," in ECCV, 2022.

[271] S. Suo, S. Regalado, S. Casas, and R. Urtasun, "Trafficsim: Learning to simulate realistic multi-agent behaviors," in CVPR, 2021.

[272] S. Tan, K. Wong, S. Wang, S. Manivasagam, M. Ren, and R. Urtasun, "Sceneg: Learning to generate realistic traffic scenes," in CVPR, 2021.

[273] H. Tang, Z. Liu, S. Zhao, Y. Lin, J. Lin, H. Wang, and S. Han, "Searching efficient 3d architectures with sparse point-voxel convolution," in ECCV, 2020.

[274] A. Tarvainen and H. Valpola, "Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results," NeurIPS, 2017.

[275] Z. Tian, C. Shen, H. Chen, and T. He, "Fcos: Fully convolutional one-stage object detection," in ICCV, 2019.

[276] J. Tu, M. Ren, S. Manivasagam, M. Liang, B. Yang, R. Du, F. Cheng, and R. Urtasun, "Physically realizable adversarial examples for lidar object detection," in CVPR, 2020.

[277] J. Tu, T. Wang, J. Wang, S. Manivasagam, M. Ren, and R. Urtasun, "Adversarial attacks on multi-agent communication," in ICCV, 2021.

[278] J. Tu, H. Li, X. Yan, M. Ren, Y. Chen, M. Liang, E. Bitar, E. Yumer, and R. Urtasun, "Exploring adversarial robustness of multi-sensor perception systems in self driving," in CoRL, 2022.

[279] N. Vadivelu, M. Ren, J. Tu, J. Wang, and R. Urtasun, "Learning to communicate and correct pose errors," in CoRL, 2021.

[280] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, "Attention is all you need," in NeurIPS, 2017.

[281] S. Vora, A. H. Lang, B. Helou, and O. Beijbom, "Pointpainting: Sequential fusion for 3d object detection," in CVPR, 2020.

[282] C. Wang, C. Ma, M. Zhu, and X. Yang, "Pointaugmenting: Cross-modal augmentation for 3d object detection," in CVPR, 2021.

[283] D. Z. Wang and I. Posner, "Voting for voting in online point cloud object detection," in RSS, 2015.

[284] H. Wang, Y. Cong, O. Litany, Y. Gao, and L. J. Guibas, "3dioamatch: Leveraging iou prediction for semi-supervised 3d object detection," in CVPR, 2021.

[285] J. Wang, S. Lan, M. Gao, and L. S. Davis, "Infofocus: 3d object detection for autonomous driving with dynamic information modeling," in ECCV, 2020.

[286] J. Wang, A. Pun, J. Tu, S. Manivasagam, A. Sadat, S. Casas, M. Ren, and R. Urtasun, "Advsim: Generating safety-critical scenarios for self-driving vehicles," in CVPR, 2021.

[287] L. Wang and B. Goldluecke, "Sparse-pointnet: See further in autonomous vehicles," IEEE RA-L, 2021.

[288] L. Wang, L. Du, X. Ye, Y. Fu, G. Guo, X. Xue, J. Feng, and L. Zhang, "Depth-conditioned dynamic message propagation for monocular 3d object detection," in CVPR, 2021.

[289] L. Wang, L. Zhang, Y. Zhu, Z. Zhang, T. He, M. Li, and X. Xue, "Progressive coordinate transforms for monocular 3d object detection," NeurIPS, 2021.

[290] Q. Wang, J. Chen, J. Deng, and X. Zhang, "3d-centernet: 3d object detection network for point clouds with center estimation priority," Pattern Recognition, 2021.

[291] S. Wang, S. Suo, W.-C. Ma, A. Pokrovsky, and R. Urtasun, "Deep parametric continuous convolutional neural networks," in CVPR, 2018.

[292] T. Wang, X. Zhu, and D. Lin, "Reconfigurable voxels: A new representation for lidar-based point clouds," arXiv preprint arXiv:200402724, 2020.

[293] T. Wang, X. Zhu, J. Pang, and D. Lin, "Fcos3d: Fully convolutional one-stage monocular 3d object detection," in ICCV, 2021.

[294] T. Wang, Z. Xinge, J. Pang, and D. Lin, "Probabilistic and geometric depth: Detecting objects in perspective," in CoRL, 2022.

[295] T.-H. Wang, S. Manivasagam, M. Liang, B. Yang, W. Zeng, and R. Urtasun, "V2vnet: Vehicle-to-vehicle communication for joint perception and prediction," in ECCV, 2020.

[296] X. Wang, W. Yin, T. Kong, Y. Jiang, L. Li, and C. Shen, "Task-aware monocular depth estimation for 3d object detection," in AAAI, 2020.

[297] Y. Wang and J. M. Solomon, "Object dgcnn: 3d object detection using dynamic graphs," NeurIPS, 2021.

[298] Y. Wang, W.-L. Chao, D. Garg, B. Hariharan, M. Campbell, and K. Q. Weinberger, "Pseudo-lidar from visual depth estimation: Bridging the gap in 3d object detection for autonomous driving," in CVPR, 2019.

[299] Y. Wang, W.-L. Chao, D. Garg, B. Hariharan, M. Campbell, and K. Q. Weinberger, "Pseudo-lidar from visual depth estimation: Bridging the gap in 3d object detection for autonomous driving," in CVPR, 2019.

[300] Y. Wang, Y. Sun, Z. Liu, S. E. Sarma, M. M. Bronstein, and J. M. Solomon, "Dynamic graph cnn for learning on point clouds," ACM TOG, 2019.

[301] Y. Wang, X. Chen, Y. You, L. E. Li, B. Hariharan, M. Campbell, K. Q. Weinberger, and W.-L. Chao, "Train in germany, test in the usa: Making 3d object detectors generalize," in CVPR, 2020.

[302] Y. Wang, A. Fathi, A. Kundu, D. A. Ross, C. Pantofaru, T. Funkhouser, and J. Solomon, "Pillar-based object detection for autonomous driving," in ECCV, 2020.

[303] Y. Wang, Q. Mao, H. Zhu, Y. Zhang, J. Ji, and Y. Zhang, "Multimodal 3d object detection in autonomous driving: a survey," arXiv preprint arXiv:210612735, 2021.

[304] Y. Wang, B. Yang, R. Hu, M. Liang, and R. Urtasun, "Plumenet: Efficient 3d object detection from stereo images," in IROS, 2021.

[305] Y. Wang, V. C. Guizilini, T. Zhang, Y. Wang, H. Zhao, and J. Solomon, "Detr3d: 3d object detection from multi-view images via 3d-to-2d queries," in CoRL, 2022.

[306] Z. Wang and K. Jia, "Frustum convnet: Sliding frustums to aggregate local point-wise features for amodal 3d object detection," in IROS, 2019.

[307] Z. Wang, S. Ding, Y. Li, J. Fenn, S. Roychowdhury, A. Wallin, L. Martin, S. Ryvola, G. Sapiro, and Q. Qiu, "Cirrus: A long-range bipartite lidar dataset," in ICRA, 2021.

[308] Z. Wang, Z. Zhao, Z. Jin, Z. Che, J. Tang, C. Shen, and Y. Peng, "Multi-stage fusion for multi-class 3d lidar detection," in ICCVW, 2021.

[309] Z. Wang, C. Min, Z. Ge, Y. Li, Z. Li, H. Yang, and D. Huang, "Sts: Surround-view temporal stereo for multi-view 3d detection," arXiv preprint arXiv:220810145, 2022.

[310] B. Wei, M. Ren, W. Zeng, M. Liang, B. Yang, and R. Urtasun, "Perceive, attend, and drive: Learning spatial attention for safe self-driving," in ICRA, 2021.

[311] Y. Wei, S. Su, J. Lu, and J. Zhou, "Fgr: Frustum-aware geometric reasoning for weakly supervised 3d vehicle detection," in ICRA, 2021.

[312] X. Weng and K. Kitani, "Monocular 3d object detection with pseudo-lidar point cloud," in ICCVW, 2019.

[313] X. Weng, Y. Man, D. Cheng, J. Park, M. O'Toole, K. Kitani, J. Wang, and D. Held, "All-in-one drive: A large-scale comprehensive perception dataset with high-density long-range point clouds," arXiv preprint, 2020.

[314] M. Wicker and M. Kwiatkowska, "Robustness of 3d deep learning in an adversarial setting," in CVPR, 2019.

[315] B. Wilson, W. Qi, T. Agarwal, J. Lambert, J. Singh, S. Khandelwal, B. Pan, R. Kumar, A. Hartnett, J. K. Pontes, et al., "Argoverse 2: Next generation datasets for self-driving perception and forecasting," in NeurIPS, 2021.

[316] K. Wong, Q. Zhang, M. Liang, B. Yang, R. Liao, A. Sadat, and R. Urtasun, "Testing the safety of self-driving vehicles by simulating perception and prediction," in ECCV, 2020.

[317] J. Wu, D. Yin, J. Chen, Y. Wu, H. Si, and K. Lin, "A survey on monocular 3d object detection algorithms based on deep learning," in Journal of Physics: Conference Series, 2020.

[318] P. Wu, S. Chen, and D. N. Metaxas, "Motionnet: Joint perception and motion prediction for autonomous driving based on bird's eye view maps," in CVPR, 2020.

[319] Y. Xiang, W. Choi, Y. Lin, and S. Savarese, "Data-driven 3d voxel patterns for object category recognition," in CVPR, 2015.

[320] Y. Xiang, W. Choi, Y. Lin, and S. Savarese, "Subcategory-aware convolutional neural networks for object proposals and detection," in WACV, 2017.

[321] P. Xiao, Z. Shao, S. Hao, Z. Zhang, X. Chai, J. Jiao, Z. Li, J. Wu, K. Sun, K. Jiang, et al., "Pandaset: Advanced sensor suite dataset for autonomous driving," in ITSC, 2021.

[322] Y. Xiao, F. Codevilla, A. Gurram, O. Urfalioglu, and A. M. Lopez, "Multimodal end-to-end autonomous driving," IEEE T-ITS, 2020.

[323] E. Xie, Z. Yu, D. Zhou, J. Philion, A. Anandkumar, S. Fidler, P. Luo, and J. M. Alvarez, "M^2bav: Multi-camera joint 3d detection and segmentation with unified birds-eye view representation," arXiv preprint arXiv:220405088, 2022.

[324] L. Xie, C. Xiang, Z. Yu, G. Xu, Z. Yang, D. Cai, and X. He, "Pi-rcnn: An efficient multi-sensor 3d object detector with point-based attentive cont-conv fusion module," in AAAI, 2020.

[325] S. Xie, J. Gu, D. Guo, C. R. Qi, L. Guibas, and O. Litany, "Pointcontrast: Unsupervised pre-training for 3d point cloud understanding," in ECCV, 2020.

[326] B. Xu and Z. Chen, "Multi-level fusion based 3d object detection from monocular images," in CVPR, 2018.

[327] D. Xu, D. Anguelov, and A. Jain, "Pointfusion: Deep sensor fusion for 3d bounding box estimation," in CVPR, 2018.

[328] Q. Xu, Y. Zhong, and U. Neumann, "Behind the curtain: Learning occluded shapes for 3d object detection," arXiv preprint arXiv:211202205, 2021.

[329] Q. Xu, Y. Zhou, W. Wang, C. R. Qi, and D. Anguelov, "Spg: Unsupervised domain adaptation for 3d object detection via semantic point generation," in ICCV, 2021.

[330] S. Xu, D. Zhou, J. Fang, J. Yin, Z. Bin, and L. Zhang, "Fusionpainting: Multimodal fusion with adaptive attention for 3d object detection," in ITSC, 2021.

[331] Z. Xu, W. Zhang, X. Ye, X. Tan, W. Yang, S. Wen, E. Ding, A. Meng, and L. Huang, "Zoomnet: Part-aware adaptive zooming neural network for 3d object detection," in AAAI, 2020.

[332] Y. Xue, J. Mao, M. Niu, H. Xu, M. B. Mi, W. Zhang, X. Wang, and X. Wang, "Point2seq: Detecting 3d objects as sequences," in CVPR, 2022.

[333] Y. Yan, Y. Mao, and B. Li, "Second: Sparsely embedded convolutional detection," Sensors, 2018.

[334] B. Yang, M. Liang, and R. Urtasun, "Hdnet: Exploiting hd maps for 3d object detection," in CoRL, 2018.

[335] B. Yang, W. Luo, and R. Urtasun, "Pixor: Real-time 3d object detection from point clouds," in CVPR, 2018.

[336] B. Yang, R. Guo, M. Liang, S. Casas, and R. Urtasun, "Radarnet: Exploiting radar for robust perception of dynamic objects," in ECCV, 2020.

[337] B. Yang, M. Bai, M. Liang, W. Zeng, and R. Urtasun, "Auto4d: Learning to label 4d objects from sequential point clouds," arXiv preprint arXiv:210106586, 2021.

[338] J. Yang, S. Shi, Z. Wang, H. Li, and X. Qi, "St3d: Self-training for unsupervised domain adaptation on 3d object detection," in CVPR, 2021.

[339] Z. Yang, Y. Sun, S. Liu, X. Shen, and J. Jia, "Ipod: Intensive point-based object detector for point cloud," arXiv preprint arXiv:181205276, 2018.

[340] Z. Yang, Y. Sun, S. Liu, X. Shen, and J. Jia, "Std: Sparse-to-dense 3d object detector for point cloud," in ICCV, 2019.

[341] Z. Yang, Y. Chai, D. Anguelov, Y. Zhou, P. Sun, D. Erhan, S. Rafferty, and H. Kretzschmar, "Surfelgan: Synthesizing realistic sensor data for autonomous driving," in CVPR, 2020.

[342] Z. Yang, Y. Sun, S. Liu, and J. Jia, "3dsd: Point-based 3d single stage object detector," in CVPR, 2020.

[343] Z. Yang, Y. Zhou, Z. Chen, and J. Ngiam, "3d-man: 3d multi-frame attention network for object detection," in CVPR, 2021.

[344] M. Ye, S. Xu, and T. Cao, "Hvnet: Hybrid voxel network for lidar based 3d object detection," in CVPR, 2020.

[345] X. Ye, L. Du, Y. Shi, Y. Li, X. Tan, J. Feng, E. Ding, and S. Wen, "Monocular 3d object detection via feature domain adaptation," in ECCV, 2020.

[346] Y. Ye, H. Chen, C. Zhang, X. Hao, and Z. Zhang, "Sarptnet: Shape attention regional proposal network for lidar-based 3d object detection," Neurocomputing, 2020.

[347] H. Yi, S. Shi, M. Ding, J. Sun, K. Xu, H. Zhou, Z. Wang, S. Li, and G. Wang, "Segvoxelnet: Exploring semantic context and depth-aware features for 3d vehicle detection from point cloud," in ICRA, 2020.

[348] Z. Yihan, C. Wang, Y. Wang, H. Xu, C. Ye, Z. Yang, and C. Ma, "Learning transferable features for point cloud detection via 3d contrastive co-training," NeurIPS, 2021.

[349] J. Yin, J. Shen, C. Guan, D. Zhou, and R. Yang, "Lidar-based online 3d video object detection with graph-based message passing and spatiotemporal transformer attention," in CVPR, 2020.

[350] T. Yin, X. Zhou, and P. Krahenbuhl, "Center-based 3d object detection and tracking," in CVPR, 2021.

[351] T. Yin, X. Zhou, and P. Krahenbuhl, "Multimodal virtual point 3d detection," NeurIPS, 2021.

[352] S. Yogamani, C. Hughes, J. Horgan, G. Sistu, P. Varley, D. O'Dea, M. Uricar, S. Milz, M. Simon, K. Amende, et al., "Woodscape: A multi-task, multi-camera fisheye dataset for autonomous driving," in ICCV, 2019.

[353] J. H. Yoo, Y. Kim, J. Kim, and J. W. Choi, "3d-cvf: Generating joint camera and lidar features using cross-view spatial feature fusion for 3d object detection," in ECCV, 2020.

[354] Y. You, Y. Wang, W.-L. Chao, D. Garg, G. Pleiss, B. Hariharan, M. Campbell, and K. Q. Weinberger, "Pseudo-lidar++: Accurate depth for 3d object detection in autonomous driving," in ICLR, 2020.

[355] Y. You, C. A. Diaz-Ruiz, Y. Wang, W.-L. Chao, B. Hariharan, M. Campbell, and K. Q. Weinberger, "Exploiting playbacks in unsupervised domain adaptation for 3d object detection," arXiv preprint arXiv:210314198, 2021.

[356] F. Yu, D. Wang, E. Shelhamer, and T. Darrell, "Deep layer aggregation," in CVPR, 2018.

[357] Z. Yuan, X. Song, L. Bai, Z. Wang, and W. Ouyang, "Temporal-channel transformer for 3d lidar-based video object detection for autonomous driving," IEEE T-CSVT, 2021.

[358] P. Yun, L. Tai, Y. Wang, C. Liu, and M. Liu, "Focal loss in 3d object detection," IEEE RA-L, 2019.

[359] S. Zakharov, W. Kehl, A. Bhargava, and A. Gaidon, "Autolabeling 3d objects with differentiable rendering of sdf shape priors," in CVPR, 2020.

[360] G. Zamanakos, L. Tsochatzidis, A. Amanatidis, and I. Pratikakis, "A comprehensive survey of lidar-based 3d object detection methods with deep learning for autonomous driving," Computers & Graphics, 2021.

[361] J. Zarzar, S. Giancola, and B. Ghanem, "Pointrcgn: Graph convolution networks for 3d vehicles detection refinement," arXiv preprint arXiv:191112236, 2019.

[362] M. Zeeshan Zia, M. Stark, and K. Schindler, "Are cars just 3d boxes?- jointly estimating the 3d shape of multiple objects," in CVPR, 2014.

[363] W. Zeng, S. Wang, R. Liao, Y. Chen, B. Yang, and R. Urtasun, "Dsdnet: Deep structured self-driving network," in ECCV, 2020.

[364] Y. Zeng, Y. Hu, S. Liu, J. Ye, Y. Han, X. Li, and N. Sun, "R3d: Realtime 3-d vehicle detection in lidar point cloud for autonomous driving," IEEE RA-L, 2018.

[365] Y. Zeng, D. Zhang, C. Wang, Z. Miao, T. Liu, X. Zhan, D. Hao, and C. Ma, "Lift: Learning 4d lidar image fusion transformer for 3d object detection," in CVPR, 2022.

[366] W. Zhang, W. Li, and D. Xu, "Srdan: Scale-aware and range-aware domain adaptation network for cross-dataset 3d object detection," in CVPR, 2021.

[367] X. Zhang, A. Zhang, J. Sun, X. Zhu, Y. E. Guo, F. Qian, and Z. M. Mao, "Emp: edge-assisted multi-vehicle perception," in MobiCom, 2021.

[368] Y. Zhang, Z. Xiang, C. Qiao, and S. Chen, "Accurate and real-time object detection based on bird's eye view on 3d point clouds," in 3DV, 2019.

[369] Y. Zhang, J. Lu, and J. Zhou, "Objects are different: Flexible monocular 3d object detection," in CVPR, 2021.

[370] Y. Zhang, J. Chen, and D. Huang, "Cat-det: Contrastively augmented transformer for multi-modal 3d object detection," in CVPR, 2022.

[371] Y. Zhang, Z. Zhu, W. Zheng, J. Huang, G. Huang, J. Zhou, and J. Lu, "Beverse: Unified perception and prediction in birds-eye-view for vision-centric autonomous driving," arXiv preprint arXiv:220509743, 2022.

[372] Z. Zhang, J. Gao, J. Mao, Y. Liu, D. Anguelov, and C. Li, "Stinet: Spatio-temporal-interactive network for pedestrian detection and trajectory prediction," in CVPR, 2020.

[373] Z. Zhang, J. Gao, J. Mao, Y. Liu, D. Anguelov, and C. Li, "Stinet: Spatio-temporal-interactive network for pedestrian detection and trajectory prediction," in CVPR, 2020.

[374] Z. Zhang, R. Girdhar, A. Joulin, and I. Misra, "Self-supervised pretraining of 3d features on any point-cloud," in ICCV, 2021.

[375] W. Zheng, W. Tang, S. Chen, L. Jiang, and C.-W. Fu, "Cia-ssd: Confident iou-aware single-stage object detector from point cloud," in AAAI, 2021.

[376] W. Zheng, W. Tang, L. Jiang, and C.-W. Fu, "Se-ssd: Self-ensembling single-stage object detector from point cloud," in CVPR, 2021.

[377] W. Zheng, W. Tang, L. Jiang, and C.-W. Fu, "Se-ssd: Self-ensembling single-stage object detector from point cloud," in CVPR, 2021.

[378] D. Zhou, J. Fang, X. Song, C. Guan, J. Yin, Y. Dai, and R. Yang, "Iou loss for 2d/3d object detection," in 3DV, 2019.

[379] D. Zhou, J. Fang, X. Song, L. Liu, J. Yin, Y. Dai, H. Li, and R. Yang, "Joint 3d instance segmentation and object detection for autonomous driving," in CVPR, 2020.

[380] X. Zhou, D. Wang, and P. Krahenbuhl, "Objects as points," arXiv preprint arXiv:190407850, 2019.

[381] X. Zhou, Y. Peng, C. Long, F. Ren, and C. Shi, "Monet3d: Towards accurate monocular 3d object localization in real time," in ICML, 2020.

[382] Y. Zhou and O. Tuzel, "Voxelnet: End-to-end learning for point cloud based 3d object detection," in CVPR, 2018.

[383] Y. Zhou, P. Sun, Y. Zhang, D. Anguelov, J. Gao, T. Ouyang, J. Guo, J. Ngiam, and V. Vasudevan, "End-to-end multi-view fusion for 3d object detection in lidar point clouds," in CoRL, 2020.

[384] Y. Zhou, Y. He, H. Zhu, C. Wang, H. Li, and Q. Jiang, "Monocular 3d object detection: An extrinsic parameter free approach," in CVPR, 2021.

[385] B. Zhu, Z. Jiang, X. Zhou, Z. Li, and G. Yu, "Class-balanced grouping and sampling for point cloud 3d object detection," arXiv preprint arXiv:190809492, 2019.

[386] J.-Y. Zhu, T. Park, P. Isola, and A. A. Efros, "Unpaired image-to-image translation using cycle-consistent adversarial networks," in ICCV, 2017.

[387] M. Zhu, C. Ma, P. Ji, and X. Yang, "Cross-modality 3d object detection," in WACV, 2021.

[388] X. Zhu, Y. Ma, T. Wang, Y. Xu, J. Shi, and D. Lin, "Ssn: Shape signature networks for multi-class object detection from point clouds," in ECCV, 2020.

[389] Y. Zhu, C. Miao, T. Zheng, F. Hajiaghajani, L. Su, and C. Qiao, "Can we use arbitrary objects to attack lidar perception in autonomous driving?," in ACM SIGSAC, 2021.

[390] Z. Zou, X. Ye, L. Du, X. Cheng, X. Tan, L. Zhang, J. Feng, X. Xue, and E. Ding, "The devil is in the task: Exploiting reciprocal appearance-localization features for monocular 3d object detection," in ICCV, 2021.
