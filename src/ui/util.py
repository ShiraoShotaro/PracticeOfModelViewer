

def drawLine(start: Tuple[int, int, int], end: Tuple[int, int, int], color: QColor, root_entity: QRoot)


    self.x_axis: Qt3DRender.QGeometry = Qt3DRender.QGeometry(self.root_entity)
    x_axis_pos: QtCore.QByteArray = QtCore.QByteArray()
    x_axis_pos.append(0)
    x_axis_pos.append(0)
    x_axis_pos.append(0)
    x_axis_pos.append(10)
    x_axis_pos.append(0)
    x_axis_pos.append(0)
    x_axis_buf: Qt3DRender.QBuffer = Qt3DRender.QBuffer(self.x_axis)
    x_axis_buf.setData(x_axis_pos)

    x_axis_attr: Qt3DRender.QAttribute = Qt3DRender.QAttribute(self.x_axis)
    x_axis_attr.setVertexBaseType(Qt3DRender.QAttribute.Float)
    x_axis_attr.setVertexSize(3)
    x_axis_attr.setAttributeType(Qt3DRender.QAttribute.VertexAttribute)
    x_axis_attr.setBuffer(x_axis_buf)
    x_axis_attr.setByteStride(3)
    x_axis_attr.setCount(2)
    self.x_axis.addAttribute(x_axis_attr)

    QByteArray bufferBytes;
	bufferBytes.resize(3 * 2 * sizeof(float)); // start.x, start.y, start.end + end.x, end.y, end.z
	float *positions = reinterpret_cast<float*>(bufferBytes.data());
	*positions++ = start.x();
	*positions++ = start.y();
	*positions++ = start.z();
	*positions++ = end.x();
	*positions++ = end.y();
	*positions++ = end.z();

	auto *buf = new Qt3DRender::QBuffer(geometry);
	buf->setData(bufferBytes);

	auto *positionAttribute = new Qt3DRender::QAttribute(geometry);
	positionAttribute->setName(Qt3DRender::QAttribute::defaultPositionAttributeName());
	positionAttribute->setVertexBaseType(Qt3DRender::QAttribute::Float);
	positionAttribute->setVertexSize(3);
	positionAttribute->setAttributeType(Qt3DRender::QAttribute::VertexAttribute);
	positionAttribute->setBuffer(buf);
	positionAttribute->setByteStride(3 * sizeof(float));
	positionAttribute->setCount(2);
	geometry->addAttribute(positionAttribute); // We add the vertices in the geometry

	// connectivity between vertices
	QByteArray indexBytes;
	indexBytes.resize(2 * sizeof(unsigned int)); // start to end
	unsigned int *indices = reinterpret_cast<unsigned int*>(indexBytes.data());
	*indices++ = 0;
	*indices++ = 1;

	auto *indexBuffer = new Qt3DRender::QBuffer(geometry);
	indexBuffer->setData(indexBytes);

	auto *indexAttribute = new Qt3DRender::QAttribute(geometry);
	indexAttribute->setVertexBaseType(Qt3DRender::QAttribute::UnsignedInt);
	indexAttribute->setAttributeType(Qt3DRender::QAttribute::IndexAttribute);
	indexAttribute->setBuffer(indexBuffer);
	indexAttribute->setCount(2);
	geometry->addAttribute(indexAttribute); // We add the indices linking the points in the geometry

	// mesh
	auto *line = new Qt3DRender::QGeometryRenderer(_rootEntity);
	line->setGeometry(geometry);
	line->setPrimitiveType(Qt3DRender::QGeometryRenderer::Lines);
	auto *material = new Qt3DExtras::QPhongMaterial(_rootEntity);
	material->setAmbient(color);

	// entity
	auto *lineEntity = new Qt3DCore::QEntity(_rootEntity);
	lineEntity->addComponent(line);
	lineEntity->addComponent(material);