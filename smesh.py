from simphony.cuds import mesh as SMesh
from simphony.core import CUBA
from mupif import Mesh
from mupif import Vertex
from mupif import Cell

class SMesh (Mesh.Mesh):
    """ 
    Mupif wrapper for Simphony Mesh class
    """
    def __init__(self, smesh):
        Mesh.__init__(self)
        if isinstance(smesh, SMesh.Mesh):
            self.smesh = smesh
        else:
            raise TypeError('smesh must be of type simphony mesh class')



        # establish mappig between integer numbering and uuids
        self._vertexUUIDMap = {}
        self._cellUUIDMap = {}
        i = 1
        for point in self.smesh._iter_points():
            self._vertexUUIDMap[i] = point.uid
            i = i+1
        # process cells (edges, faces, cells):
        i = 1
        for edge in self.smesh._iter_edges():
            self._cellUUIDMap[i] = edge.uid
            i = i+1
        for face in self.smesh._iter_faces():
            self._cellUUIDMap[i] = face.uid
            i = i+1
        for cell in self.smesh._iter_cells():
            self._cellUUIDMap[i] = cell.uid
            i = i+1            
            


    def getNumberOfVertices(self):
        return self.smesh.count_of(CUBA.POINT)

    
    def getNumberOfCells(self):
        return (self.smesh.count_of(CUBA.EDGE)+
                self.smesh.count_of(CUBA.FACE)+
                self.smesh.count_of(CUBA.CELL))
    
    def getVertex(self, i):
        """
        The index here is uuid, not int -> check
        spoint.data -> metadata; how to map this to mupif?
        """
        spoint = self.smesh._get_point(self._vertexUUIDMap[i])
        return Vertex.Vertex(i, i, coords=spoint.coordinates)

    def getCell (self, i):
        """
        The index here is uuid, not int -> check
        """
        
        # need to deal with separate lists of edges, faces and cells on Simphony side
        uuid = self._cellUUIDMap[i]
        try:
            edge = self.smesh._get_edge(uuid)
            # no support for edges yet
            cell = self._EdgeElement(len(edge.points)) (i, i, edge.points)
        except KeyError:
            cell = None

        if (!cell):
            try:
                face = self.smesh._get_face(uuid)
                cell = self._FaceElement(len(face.points)) (i, i, face.points)
            except KeyError:
                cell = None

        if (!cell):
            try:
                scell = self.smesh._get_cell(uuid)
                cell = self._CellElement(len(scell.points)) (i, i, scell.points)
            except KeyError:
                cell = None

        if (cell):
            return cell
        else:
            raise KeyError('cell id not found')
                
    def _EdgeElement(self, nn):
         """
         Return mupif cell class corresponding to edge with given number of nodes
         :param:nvert number of nodes/vertices
         """
         raise TypeError('unsupported number of vertices')
         

    def _FaceElement(self, nn):
        """
        Return mupif cell class corresponding to face with given number of nodes
        :param:nvert number of nodes/vertices
        """
        if (nn == 3):
            return Cell.Triangle_2d_lin
        else if (nn == 4):
            return Cell.Quad_2d_lin
        else if (nn == 6):
            return Triangle_2d_quad
        else:
            raise TypeError('unsupported number of vertices')

    def _CellElement(self, nn):
        """
        Return mupif cell class corresponding to cell with given number of nodes
        :param:nvert number of nodes/vertices
        """
        if nn==4:
            return Cell.Tetrahedron_3d_lin
        else if nn==8:
            return Cell.Brick_3d_lin
        else:
            raise TypeError('unsupported number of vertices')
        

        

        
        
