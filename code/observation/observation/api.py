from io import BytesIO
import cherrypy as cp

from observation import Observation, ObservationError


class ObservationLoader(object):
    def __init__(self, tsdb):
        self.tsdb = tsdb

    @cp.expose
    @cp.tools.json_out()
    @cp.tools.allow(methods=['POST'])
    def index(self):
        data = BytesIO(cp.request.body.read())
        try:
            my_obs = Observation(data)
        except ObservationError as e:
            return dict(error="Error happened reading: {}".format(e))

        meta = my_obs.meta()
        for i in my_obs.data_with_time():
            # TODO Use API, not direct
            self.tsdb.send(
                metric=meta['channel'],
                value=i[1],
                timestamp=i[0],
                network=meta['network'],
                station=meta['station'])
        self.tsdb.close()
        meta_out=dict(
            network=meta['network'],
            station=meta['station'],
            channel=meta['channel'],
            start=str(meta['starttime']),
            end=str(meta['endtime']),
            sampling_rate=meta['sampling_rate'],
        )
        return dict(status="ok", meta=meta_out)
