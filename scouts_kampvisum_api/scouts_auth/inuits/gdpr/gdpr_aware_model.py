class GDPRAware:
    def remove_sensitive_information(self):
        """
        Removes sensitive data from the database.

        Since some models perform a soft delete without an implementor being
        aware of this, it is recommended to replace sensitive data with null
        values in the database, performing a save, then a delete.
        """
        # Code should not reach this
        raise NotImplementedError("This GDPR aware class has an invalid implementation")

    def remove_sensitive_files(self):
        """
        Removes any and all files that should be deleted.
        """
        # Code should not reach this
        raise NotImplementedError("This GDPR aware class has an invalid implementation")
