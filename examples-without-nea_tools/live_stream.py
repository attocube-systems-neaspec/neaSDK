"""Helpers for streaming microscope data into a tab-separated export file."""

from time import time, sleep
import os
from typing import Dict, List, Optional
import System
from neaspec import context


class Stream:
    """Collect demodulated data samples and write them to a TSV file."""

    def __init__(self, fname: str, channels: Optional[List[str]] = None):
        """Initialize the stream with a target export path and channel list.

        Args:
            fname: Path to the export file that will be created.
            channels: Optional explicit channel order to export. When omitted,
                the stream uses the full default set of available measurements.
        """
        if channels is None:
            self.channels = [
                "time", "AveragedX", "AveragedY", "AveragedZ", "AveragedM",
                "Row", "Column", "Depth",
                "HeadFrequency", "MirrorFrequency", "LaserTriggerFrequency", "SlaveMirrorFrequency",
                "HeadAmplitude", "MirrorAmplitude", "LaserTriggerAmplitude", "SlaveMirrorAmplitude",
                "HeadOffset", "MirrorOffset", "LaserTriggerOffset", "SlaveMirrorOffset",
                "M0A", "M0P", "M1A", "M1P", "M2A", "M2P", "M3A", "M3P", "M4A", "M4P", "M5A", "M5P",
                "O0A", "O0P", "O1A", "O1P", "O2A", "O2P", "O3A", "O3P", "O4A", "O4P", "O5A", "O5P",
                "A0A", "A0P", "A1A", "A1P", "A2A", "A2P", "A3A", "A3P", "A4A", "A4P", "A5A", "A5P",
                "B0A", "B0P", "B1A", "B1P", "B2A", "B2P", "B3A", "B3P", "B4A", "B4P", "B5A", "B5P",
                "EA", "EP"
            ]
        else:
            self.channels = channels
        self._file = None
        self.fname = fname
        self._time_started = time()
        self.data: Dict[str, List[float]] = {}
        self._new_data: Dict[str, float] = {}
        self._header_written = False
        self._reset_channels()

    def __enter__(self):
        """Start the stream and return itself for use in a context manager."""
        self.run()
        return self

    def __exit__(self, *args):
        """Stop the stream when leaving a context manager."""
        self.stop()

    def _reset_channels(self):
        """Clear any collected samples and recreate empty lists for each channel."""
        self.data.clear()
        [self.data.update({channel: []}) for channel in self.channels]

    def _convert_to_floats(self):
        """Convert stored .NET Single values to native Python floats."""
        for key, data in self.data.items():
            if not isinstance(data[0], System.Single):
                continue
            self.data[key] = [float(value) for value in data]

    def run(self):
        """Open the export file and subscribe to incoming microscope data."""
        self._time_started = time()
        self._file = open(str(self.fname), "w", encoding="ascii")
        context.Microscope.DataDemodulated += self.on_data_demodulated
        self.write_header()
        print("Stream: running")

    def stop(self):
        """Unsubscribe from the data stream and write the collected samples."""
        context.Microscope.DataDemodulated -= self.on_data_demodulated
        self._convert_to_floats()
        self.write_channels()
        if self._file is not None:
            self._file.close()
        print("Stream: stopped")

    def write_channels(self):
        """Write all collected rows to the export file."""
        if self._file is None:
            raise IOError("Export file not opened")
        length = len(self.data[self.channels[0]])
        print("Stream: writing lines - ", length)
        for index in range(length):
            line = "\t".join(str(self.data[key][index])
                             for key in self.channels)+"\n"
            self._file.write(line)

    def write_header(self):
        """Write the header row once for the exported TSV file."""
        print("Stream: writing header")
        if self._header_written:
            raise IOError("Header already written to export file.")
        if self._file is None:
            raise IOError("Export file not opened")
        col_label = "\t".join(self.channels)+"\n"
        self._file.write(col_label)
        self._header_written = True

    def on_data_demodulated(self, _, args):
        """Handle incoming demodulated data events by copying them into storage."""
        self.copy_channels(args)

    def copy_channels(self, args):
        """Copy the latest microscope values into the internal sample buffer."""
        self._new_data['time'] = time()-self._time_started
        self._new_data['AveragedX'] = args.AveragedX
        self._new_data['AveragedY'] = args.AveragedY
        self._new_data['AveragedZ'] = args.AveragedZ
        self._new_data['AveragedM'] = args.AveragedM
        self._new_data['Row'] = args.Row
        self._new_data['Column'] = args.Column
        self._new_data['Depth'] = args.Depth
        self._new_data['HeadFrequency'] = args.HeadFrequency
        self._new_data['MirrorFrequency'] = args.MirrorFrequency
        self._new_data['LaserTriggerFrequency'] = args.LaserTriggerFrequency
        self._new_data['SlaveMirrorFrequency'] = args.SlaveMirrorFrequency
        self._new_data['HeadAmplitude'] = args.HeadAmplitude
        self._new_data['MirrorAmplitude'] = args.MirrorAmplitude
        self._new_data['LaserTriggerAmplitude'] = args.LaserTriggerAmplitude
        self._new_data['SlaveMirrorAmplitude'] = args.SlaveMirrorAmplitude
        self._new_data['HeadOffset'] = args.HeadOffset
        self._new_data['MirrorOffset'] = args.MirrorOffset
        self._new_data['LaserTriggerOffset'] = args.LaserTriggerOffset
        self._new_data['SlaveMirrorOffset'] = args.SlaveMirrorOffset
        self._new_data['M0A'] = args.Mechanical[0]
        self._new_data['M0P'] = args.Mechanical[1]
        self._new_data['M1A'] = args.Mechanical[2]
        self._new_data['M1P'] = args.Mechanical[3]
        self._new_data['M2A'] = args.Mechanical[4]
        self._new_data['M2P'] = args.Mechanical[5]
        self._new_data['M3A'] = args.Mechanical[6]
        self._new_data['M3P'] = args.Mechanical[7]
        self._new_data['M4A'] = args.Mechanical[8]
        self._new_data['M4P'] = args.Mechanical[9]
        self._new_data['M5A'] = args.Mechanical[10]
        self._new_data['M5P'] = args.Mechanical[11]
        self._new_data['O0A'] = args.Optical[0]
        self._new_data['O0P'] = args.Optical[1]
        self._new_data['O1A'] = args.Optical[2]
        self._new_data['O1P'] = args.Optical[3]
        self._new_data['O2A'] = args.Optical[4]
        self._new_data['O2P'] = args.Optical[5]
        self._new_data['O3A'] = args.Optical[6]
        self._new_data['O3P'] = args.Optical[7]
        self._new_data['O4A'] = args.Optical[8]
        self._new_data['O4P'] = args.Optical[9]
        self._new_data['O5A'] = args.Optical[10]
        self._new_data['O5P'] = args.Optical[11]
        self._new_data['A0A'] = args.A[0]
        self._new_data['A0P'] = args.A[1]
        self._new_data['A1A'] = args.A[2]
        self._new_data['A1P'] = args.A[3]
        self._new_data['A2A'] = args.A[4]
        self._new_data['A2P'] = args.A[5]
        self._new_data['A3A'] = args.A[6]
        self._new_data['A3P'] = args.A[7]
        self._new_data['A4A'] = args.A[8]
        self._new_data['A4P'] = args.A[9]
        self._new_data['A5A'] = args.A[10]
        self._new_data['A5P'] = args.A[11]
        self._new_data['B0A'] = args.B[0]
        self._new_data['B0P'] = args.B[1]
        self._new_data['B1A'] = args.B[2]
        self._new_data['B1P'] = args.B[3]
        self._new_data['B2A'] = args.B[4]
        self._new_data['B2P'] = args.B[5]
        self._new_data['B3A'] = args.B[6]
        self._new_data['B3P'] = args.B[7]
        self._new_data['B4A'] = args.B[8]
        self._new_data['B4P'] = args.B[9]
        self._new_data['B5A'] = args.B[10]
        self._new_data['B5P'] = args.B[11]
        self._new_data['EA'] = args.Electrical[0]
        self._new_data['EP'] = args.Electrical[1]
        for channel, data in self.data.items():
            data.append(self._new_data[channel])


# Record channels time, Z, M1A, M1P, O2A, and O2P for 10 sec
# and write them to Desktop/live_stream.txt file
channels = ["time", "AveragedZ", "M1A", "M1P", "O2A", "O2P"]
fname = os.path.expanduser(r"~\Desktop\live_stream.txt")
with Stream(fname, channels) as stream:
    sleep(10)