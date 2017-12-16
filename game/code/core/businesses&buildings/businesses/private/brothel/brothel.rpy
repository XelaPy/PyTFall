init -5 python:
    class BrothelBlock(PrivateBusiness):
        SORTING_ORDER = 5
        COMPATIBILITY = []
        MATERIALS = {"Wood": 70, "Bricks": 30, "Glass": 5}
        ID = "Brothel"
        IMG = "content/buildings/upgrades/room.jpg"
        def __init__(self, name="Brothel", instance=None, desc="Rooms to freck in!",
                     img="content/buildings/upgrades/room.jpg", **kwargs):

            super(BrothelBlock, self).__init__(name=name, instance=instance,
                        desc=desc, img=img, **kwargs)

            self.type = "personal_service"
            self.jobs = set([simple_jobs["Whore Job"]])
            self.workable = True

            # SimPy and etc follows:
            self.res = None # Restored before every job...
            self.time = 5 # Same
            self.is_running = False # Is true when the business is running, this is being set to True at the start of the ND and to False on it's end.

        def has_workers(self):
            # Check if the building still has someone available to do the job.
            # We just check this for
            return list(i for i in building.available_workers if self.all_occs & i.occupations)

        def business_control(self):
            while 1:
                yield self.env.timeout(self.time)

                if self.res.count == 0 and not self.has_workers():
                    break

            # We remove the business from nd if there are no more strippers to entertain:
            temp = "There are no workers available in the {} so it is shutting down!".format(self.name)
            self.log(temp)
            building.nd_ups.remove(self)

        def request_resource(self, client, worker):
            """Requests a room from Sim'Py, under the current code, this will not be called if there are no rooms available...

            If the above docstring is true, and this is never called if there are no rooms, while do we request shit?
            ==> This is likely capacity related. Should be working just fine.
            """
            with self.res.request() as request:
                yield request

                # All is well and the client enters:
                temp = "{}: {} and {} enter the room.".format(self.env.now, client.name, worker.name)
                self.log(temp)

                # This line will make sure code halts here until run_job ran it's course...
                yield self.env.timeout(self.time)
                result = self.run_job(client, worker)

                if result >= 150:
                    line = "The service was excellent!"
                elif result >= 100:
                    line = "The service was good!"
                elif result >= 50:
                    line = "The service was 'meh'."
                else:
                    line = "The service was shit."
                temp = "{} 'did' {}... {}".format(
                            set_font_color(worker.name, "pink"),
                            client.name,
                            line)
                self.log(temp, True)
                temp = "{} leaves the {}.".format(client.name, self.name)
                self.log(temp, True)
                # client.flag("jobs_busy").interrupt()
            client.del_flag("jobs_busy")

        def run_job(self, client, worker):
            """Handles the job and job report.
            """
            # Visit counter:
            client.up_counter("got_serviced_by" + worker.id)

            # Execute the job/log results/handle finances and etc.:
            job, building = self.job, building
            log = NDEvent(job=job, char=worker, loc=building, business=self)
            worker.jobpoints -= 100
            job.settle_workers_disposition(worker, log)

            difficulty = building.tier
            effectiveness = job.effectiveness(worker, difficulty, log, False)

            result = job.work_brothel(worker=worker, client=client, building=building, log=log, effectiveness=effectiveness)

            earned = payout(job, effectiveness, difficulty, building, self, worker, client, log)

            log.after_job()
            NextDayEvents.append(log)

            # We return the char to the nd list:
            building.available_workers.insert(0, worker)
            return result
